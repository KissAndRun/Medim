import SimpleITK as sitk
import configparser
import sys
import os
import ast

def readConfig(configFile):
    config = myReader()
    config.read(configFile)
    transform = config.get('base', 'transform')
    optimizer = config.get('base', 'optimizer')
    interpolator = config.get('base', 'interpolator')
    metric = config.get('base', 'metric')
    bins = config.get('Similarity', 'numberOfHistogramBins')
    parm = config.items(optimizer)
    args = {a[0]:ast.literal_eval(a[1]) for a in parm}
    conf = {"transform":transform,
            "optimizer":optimizer,
            "interpolator":interpolator,
            "metric":metric,
            "bins":ast.literal_eval(bins),
            "args":args}
    print(conf)
    return conf

def command_iteration(method) :
    print("{0:3} = {1:10.5f}".format(method.GetOptimizerIteration(),
                                     method.GetMetricValue()))

def _initialTransform(fixed, moving, conf):
    transfromDomainMeshSize=[8]*moving.GetDimension()
    if conf['transform'] == 'BSplineTransform':
        tx = sitk.BSplineTransformInitializer(fixed, transfromDomainMeshSize)
    elif conf['transform'] == 'AffineTransform':
        tx = sitk.CenteredTransformInitializer(fixed, moving,
                    sitk.AffineTransform(moving.GetDimension()),
                    sitk.CenteredTransformInitializerFilter.GEOMETRY)
    else:
        tx = sitk.CenteredTransformInitializer(fixed, moving,
                    getattr(sitk,conf['transform'])(),
                    sitk.CenteredTransformInitializerFilter.GEOMETRY)
    return tx

def _setTransform(tx, fixed, moving, conf):
    R = sitk.ImageRegistrationMethod()
    if conf['metric']=='MattesMutualInformation':
        getattr(R,'SetMetricAs'+conf['metric'])(conf['bins'])
    else:
        getattr(R,'SetMetricAs'+conf['metric'])()
    getattr(R,'SetOptimizerAs'+conf['optimizer'])(**conf['args'])
    R.SetShrinkFactorsPerLevel(shrinkFactors=[4, 2, 1])
    R.SetSmoothingSigmasPerLevel(smoothingSigmas=[2, 1, 0])
    R.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
    R.SetInitialTransform(tx, True)
    R.SetInterpolator(getattr(sitk,'sitk'+conf['interpolator']))
    R.AddCommand(sitk.sitkIterationEvent, lambda: command_iteration(R))
    outTx = R.Execute(fixed, moving)
    return outTx

def _resampler(fixed, moving, outTx):
    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed);
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(100.)
    resampler.SetTransform(outTx)
    out = resampler.Execute(moving)
    return out

def _caster(fixed, out):
    simg1 = sitk.GetArrayFromImage(fixed)
    simg2 = sitk.GetArrayFromImage(out)
    simg3 = simg1/2. + simg2/2.
    return simg3

def getReg(fixed, moving, conf):
    tx = _initialTransform(fixed, moving, conf)
    outTx = _setTransform(tx, fixed, moving, conf)
    out = _resampler(fixed, moving, outTx)
    cimg = _caster(fixed, out)
    return cimg

class myReader(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    # 这里重写了optionxform方法，直接返回选项名
    def optionxform(self, optionstr):
        return optionstr

if __name__ == '__main__':
    if len ( sys.argv ) < 4:
        print( "Usage: {0} <fixedImageFile> <movingImageFile> <configFile>".format(sys.argv[0]))
        sys.exit(1)
    conf = readConfig(sys.argv[3])
    fixed = sitk.ReadImage(sys.argv[1], sitk.sitkFloat32)
    moving = sitk.ReadImage(sys.argv[2], sitk.sitkFloat32)
    re = getReg(fixed, moving, conf)
    result = sitk.GetImageFromArray(re)
    #sitk.Show(result)
    sitk.WriteImage(result,"./Result.mhd")
