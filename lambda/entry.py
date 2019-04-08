import matplotlib
matplotlib.use('agg')

import csv
import json
import numpy as np
import matplotlib.pyplot as plt
from boto3.session import Session
from mpl_toolkits.basemap import Basemap
from os import environ, remove
from PIL import Image

aws = Session()
s3 = aws.resource('s3')
bucket = s3.Bucket(environ['OUTPUT_BUCKET'])

desc = 'Temperature (°F)'
lats = [42.467, 42.5086, 42.4358, 42.4269, 42.4721, 42.4544, 42.4907, 42.4818, 42.5328, 42.5278, 42.7008, 42.6921, 42.6834, 42.6746, 42.7367, 42.7194, 42.7107, 42.6324, 42.738, 42.7117, 42.9201, 42.9029, 42.9157, 42.907, 42.8983, 42.8895, 42.9516, 42.9343, 42.9256, 42.976, 42.9028, 42.9391, 42.4009, 42.3281, 42.3192, 42.3645, 42.3467, 42.383, 42.3742, 42.4425, 42.4251, 42.4202, 42.5932, 42.5846, 42.567, 42.6292, 42.6032, 42.6535, 42.5805, 42.6404, 42.6851, 42.6764, 42.8127, 42.7955, 42.8313, 42.7495, 42.8442, 42.8269, 42.8182, 42.8686, 42.7954, 42.8318, 42.8229, 43.0275, 43.0103, 43.0461, 42.9732, 42.9642, 42.3692, 42.3879, 42.4239, 42.4655, 42.3927, 42.3838, 42.4785, 42.4698, 42.4612, 42.4299, 42.4662, 42.4848, 42.5345, 42.695, 42.6218, 42.613, 42.6042, 42.6808, 42.6169, 42.608, 42.6443, 42.6265, 42.7996, 42.8367, 42.828, 42.8192, 42.8728, 42.8553, 42.8465, 42.9099, 42.9783, 43.0144, 42.4309, 42.4261, 42.4172, 42.4856, 42.4682, 42.5215, 42.5129, 42.5043, 42.5488, 42.5402, 42.4669, 42.6599, 42.651, 42.6873, 42.6784, 42.6695, 42.6593, 42.5775, 42.6722, 42.6462, 42.6908, 42.6822, 42.8743, 42.7925, 42.8377, 42.8884, 42.8797, 42.8621, 42.8747, 42.8658, 42.8932, 42.8843, 42.3952, 42.3222, 42.3586, 42.3771, 42.5502, 42.5415, 42.524, 42.5367, 42.5189, 42.5875, 42.5612, 42.5973, 42.7293, 42.7205, 42.7653, 42.7566, 42.7479, 42.7391, 42.8069, 42.725, 42.8256, 42.7525, 42.9845, 42.9673, 43.0031, 42.9302, 42.9213, 43.0404, 42.9672, 42.3488, 42.3937, 42.385, 42.3674, 42.421, 42.4036, 42.576, 42.563, 42.5455, 42.6134, 42.6048, 42.5315, 42.632, 42.6234, 42.559, 42.6235, 42.7553, 42.7467, 42.7912, 42.774, 42.7518, 42.7429, 42.734, 42.7791, 42.7703, 42.8471, 42.774, 42.8524, 42.9206, 42.9117, 42.9568, 42.9576, 42.9487, 43.0027, 42.9939, 42.4037, 42.3866, 42.4224, 42.3497, 42.3407, 42.386, 42.3682, 42.4368, 42.428, 42.4105, 42.4232, 42.5787, 42.57, 42.6148, 42.6061, 42.5886, 42.6564, 42.5745, 42.652, 42.6433, 42.6257, 42.6619, 42.7983, 42.7897, 42.8342, 42.817, 42.8298, 42.8211, 42.8123, 42.8036, 42.8714, 42.7895, 42.89, 42.8169, 43.0218, 43.0131, 42.9398, 43.0489, 43.0317, 42.4525, 42.5114, 42.5029, 42.4943, 42.5301, 42.4573, 42.4484, 42.4937, 42.4759, 42.5444, 42.5181, 42.5308, 42.6863, 42.6775, 42.6687, 42.7223, 42.7136, 42.7049, 42.6961, 42.599, 42.7235, 42.7595, 42.8641, 42.9144, 42.9058, 42.8324, 42.9012, 42.8924, 42.8836, 42.9372, 42.9197, 42.911, 42.9243, 42.4477, 42.4388, 42.4839, 42.52, 42.5025, 42.5703, 42.4885, 42.5659, 42.5572, 42.5396, 42.7123, 42.7037, 42.7482, 42.731, 42.7496, 42.7854, 42.7035, 42.8592, 42.8414, 42.9273, 42.9186, 42.9631, 42.9459, 42.9147, 42.9598, 42.9509, 42.3576, 42.4623, 42.4985, 42.4809, 42.5171, 42.5675, 42.5589, 42.4944, 42.5717, 42.5543, 42.7267, 42.7095, 42.7453, 42.6635, 42.7639, 42.682, 42.7826, 42.7095, 42.7879, 42.8562, 42.8473, 42.9416, 42.9244, 42.9602, 42.8784, 42.9383, 42.9295, 42.9743, 42.9656, 42.948, 42.3663, 42.4023, 42.4075, 42.3898, 42.4842, 42.4756, 42.4024, 42.4447, 42.4633, 42.5083, 42.4995, 42.5679, 42.7281, 42.6363, 42.6276, 42.6188, 42.6101, 42.6228, 42.605, 42.6413, 42.7829, 42.8513, 42.8426, 42.8338, 42.825, 42.8872, 42.8699, 42.8611, 42.9115, 42.8384, 42.943, 42.9929, 43.0114, 42.4554, 42.5057, 42.4971, 42.4239, 42.533, 42.5244, 42.5158, 42.5516, 42.4789, 42.4699, 42.5299, 42.5211, 42.516, 42.6717, 42.6628, 42.7078, 42.699, 42.6902, 42.5894, 42.6836, 42.6205, 42.7449, 42.8044, 42.9087, 42.9, 42.8913, 42.8865, 42.8777, 42.9227, 42.9139, 42.9051, 42.4193, 42.487, 42.4143, 42.4054, 42.4653, 42.4565, 42.5014, 42.4926, 42.4751, 42.5287, 42.5113, 42.7209, 42.639, 42.7396, 42.6665, 42.6478, 42.6392, 42.6345, 42.6793, 42.6706, 42.6531, 42.8628, 42.8542, 42.8986, 42.8814, 42.8503, 42.9359, 42.8539, 42.9545, 42.8813, 43.0045, 42.398, 42.3894, 42.3162, 42.4253, 42.4081, 42.444, 42.3712, 42.3623, 42.4222, 42.4134, 42.4813, 42.4083, 42.5553, 42.5464, 42.6003, 42.5915, 42.6421, 42.6374, 42.6286, 42.6735, 42.6472, 42.6969, 42.8012, 42.7839, 42.7752, 42.8198, 42.8112, 42.7465, 42.8153, 42.8065, 42.7977, 42.8571, 42.8929, 42.9616, 43.016, 42.9987, 43.0432, 43.0346, 42.9612, 42.4454, 42.4408, 42.5, 42.4914, 42.4827, 42.5273, 42.5187, 42.4454, 42.5545, 42.5459, 42.5373, 42.5063, 42.6658, 42.6569, 42.648, 42.6932, 42.6843, 42.6607, 42.7051, 42.8259, 42.8942, 42.8768, 42.8806, 42.8718, 42.8629, 42.908, 42.8992, 42.4506, 42.4328, 42.4692, 42.4603, 42.5054, 42.556, 42.5473, 42.5514, 42.5426, 42.7152, 42.6979, 42.6892, 42.7338, 42.7252, 42.7711, 42.9172, 42.8444, 42.8354, 42.9301, 42.9128, 42.9041, 42.9487, 42.9401, 42.8754, 42.9177, 42.9362, 42.474, 42.51, 42.5152, 42.4974, 42.5918, 42.5833, 42.51, 42.5709, 42.6754, 42.7029, 42.694, 42.7303, 42.7214, 42.7125, 42.781, 42.8855, 42.868, 42.8903, 42.9587, 42.9412, 42.9946, 42.9859, 42.9772, 42.3808, 42.4046, 42.3957, 42.4899, 42.4727, 42.4417, 42.4868, 42.478, 42.5229, 42.5142, 42.4966, 42.7066, 42.7424, 42.6605, 42.6507, 42.6334, 42.6247, 42.6198, 42.6109, 42.6648, 42.656, 42.8657, 42.8484, 42.8397, 42.8843, 42.8757, 42.8109, 42.8533, 42.9215, 42.9573, 42.99, 43.026, 42.3547, 42.3908, 42.4094, 42.4684, 42.4598, 42.4512, 42.4641, 42.4467, 42.4379, 42.4514, 42.4878, 42.6191, 42.556, 42.6805, 42.7165, 42.6071, 42.5983, 42.6751, 42.6664, 42.7023, 42.6384, 42.6295, 42.7399, 42.8528, 42.771, 42.8221, 42.8133, 42.8582, 42.8495, 42.8406, 42.8953, 42.9314, 42.9636, 42.9547, 42.9997, 42.4339, 42.4163, 42.4291, 42.4113, 42.4798, 42.4711, 42.4535, 42.5071, 42.4897, 42.5431, 42.5344, 42.5258, 42.7181, 42.645, 42.6814, 42.6725, 42.6621, 42.6449, 42.6578, 42.6491, 42.6316, 42.6937, 42.6677, 42.8771, 42.8599, 42.8958, 42.8139, 42.8739, 42.8651, 42.933, 42.8599, 42.8962, 42.8873, 42.3837, 42.4382, 42.3653, 42.4885, 42.5122, 42.5976, 42.589, 42.5804, 42.5494, 42.5944, 42.5856, 42.6539, 42.7088, 42.6999, 42.691, 42.7362, 42.7273, 42.8141, 42.8094, 42.8826, 42.8688, 42.9731, 42.9644, 42.9558, 43.0003, 42.9917, 42.9183, 42.3779, 42.3605, 42.3517, 42.4138, 42.4052, 42.3966, 42.4411, 42.4325, 42.3593, 42.4016, 42.5746, 42.6162, 42.5523, 42.5434, 42.5797, 42.562, 42.6305, 42.6354, 42.7668, 42.685, 42.7723, 42.7635, 42.7547, 42.8083, 42.7909, 42.7821, 42.7947, 42.7859, 42.7769, 42.8455, 42.95, 42.9324, 42.9685, 42.9958, 42.9871, 42.9695, 43.0231, 43.0056, 42.9968, 42.34, 42.3311, 42.3762, 42.4123, 42.3948, 42.4626, 42.4541, 42.3808, 42.4583, 42.4496, 42.432, 42.4729, 42.5961, 42.6406, 42.702, 42.6012, 42.5924, 42.5835, 42.6779, 42.6693, 42.596, 42.6966, 42.688, 42.7614, 42.8556, 42.8385, 42.8162, 42.8073, 42.7984, 42.8436, 42.8347, 42.9168, 42.9665, 42.985, 42.9761, 42.4769, 42.4594, 42.4955, 42.5316, 42.5732, 42.5093, 42.5004, 42.5861, 42.5775, 42.5688, 42.5375, 42.7238, 42.642, 42.7611, 42.688, 42.7244, 42.7155, 42.7664, 42.8025, 42.8709, 42.9387, 42.8569, 42.9021, 42.9529, 42.9441, 42.9265, 42.9801, 42.9627, 42.9812, 42.4167, 42.3437, 42.3801, 42.5357, 42.5269, 42.5947, 42.5219, 42.513, 42.5729, 42.5641, 42.609, 42.5827, 42.7147, 42.7058, 42.7508, 42.742, 42.7332, 42.7926, 42.8284, 42.824, 42.8971, 42.9285, 42.9788, 42.9702, 42.8968, 43.006, 42.9974, 42.9888, 43.0074, 42.3429, 42.3615, 42.3526, 42.3977, 42.4569, 42.4483, 42.4396, 42.4437, 42.4349, 42.6076, 42.5816, 42.6263, 42.6177, 42.5953, 42.5865, 42.6636, 42.6549, 42.6994, 42.6175, 42.8098, 42.728, 42.7732, 42.8413, 42.8327, 42.8103, 42.8014, 42.8288, 42.8199, 43.0246, 42.9517, 42.9428, 42.988, 42.9702, 42.3341, 42.3252, 42.3791, 42.3703, 42.4152, 42.4065, 42.3889, 42.5617, 42.5531, 42.5485, 42.599, 42.5904, 42.6349, 42.553, 42.7582, 42.7409, 42.7322, 42.7768, 42.7682, 42.7458, 42.7369, 42.7644, 42.7555, 42.8499, 42.768, 42.9236, 42.9058, 42.9421, 42.9332, 42.9606, 42.9791, 42.337, 42.3556, 42.4007, 42.3919, 42.5646, 42.5386, 42.5338, 42.5249, 42.5758, 42.6205, 42.6119, 42.7438, 42.7351, 42.7264, 42.7176, 42.7797, 42.7624, 42.7537, 42.8041, 42.731, 42.7673, 42.7584, 42.8356, 42.9817, 42.9088, 42.8998, 42.9451, 42.9273, 43.0189, 42.9457, 42.9821, 42.3923, 42.375, 42.4196, 42.411, 42.3378, 42.4468, 42.4296, 42.3987, 42.5034, 42.5582, 42.5405, 42.5768, 42.6139, 42.6589, 42.6502, 42.7184, 42.7868, 42.7781, 42.7694, 42.7606, 42.8227, 42.8054, 42.7967, 42.8006, 42.7918, 42.8785, 42.947, 42.983, 43.0016, 42.9841, 42.9754, 43.0375, 43.0288, 43.0202, 42.3721, 42.3634, 42.3459, 42.3995, 42.382, 42.3733, 42.4354, 42.4268, 42.4181, 42.3868, 42.4915, 42.5601, 42.6105, 42.6019, 42.6377, 42.5738, 42.5649, 42.6159, 42.602, 42.7697, 42.7525, 42.7883, 42.7065, 42.7576, 42.7488, 42.7938, 42.785, 42.7762, 42.7888, 42.7799, 42.8309, 42.867, 42.9354, 42.9714, 42.9539, 42.9724, 43.0173, 43.0085, 42.9909]
lons = [-76.9485, -77.1491, -76.4192, -76.3317, -76.5611, -76.386, -76.5279, -76.4404, -76.7283, -76.4615, -76.8761, -76.7883, -76.7006, -76.6128, -77.0186, -76.8429, -76.7551, -76.4122, -76.8097, -76.5463, -77.1046, -76.9286, -76.8367, -76.7487, -76.6608, -76.5728, -76.9794, -76.8034, -76.7154, -77.0048, -76.2717, -76.4142, -77.1684, -76.4393, -76.3519, -76.5811, -76.4062, -76.5479, -76.4604, -76.9232, -76.7481, -76.4816, -76.8958, -76.8081, -76.6328, -77.0381, -76.7749, -77.0634, -76.3326, -76.7085, -76.9386, -76.8508, -77.124, -76.9482, -77.0908, -76.2709, -76.999, -76.8232, -76.7353, -77.0244, -76.292, -76.4344, -76.3465, -77.0851, -76.9089, -77.0518, -76.3181, -76.2301, -76.8475, -76.8144, -76.9563, -77.1568, -76.4273, -76.3398, -77.0653, -76.9777, -76.8901, -76.3609, -76.5027, -76.4695, -76.3115, -76.8176, -76.7417, -76.654, -76.5663, -77.118, -76.4747, -76.387, -76.5291, -76.3537, -76.7685, -76.702, -76.6141, -76.5263, -76.8446, -76.6687, -76.5808, -76.778, -76.5861, -76.7288, -76.8065, -76.5399, -76.4524, -76.9154, -76.7402, -77.0575, -76.9699, -76.8823, -77.1121, -77.0244, -76.2944, -76.4666, -76.3789, -76.5211, -76.4333, -76.3456, -77.1219, -76.3034, -77.0303, -76.767, -76.9971, -76.9093, -77.083, -76.2628, -76.493, -76.782, -76.6941, -76.5182, -76.4263, -76.3384, -76.393, -76.305, -77.11, -76.381, -76.5228, -76.4896, -76.9036, -76.816, -76.6407, -76.5491, -76.3739, -76.8373, -76.5743, -76.7165, -76.7219, -76.6341, -76.8643, -76.7765, -76.6886, -76.6008, -77.0654, -76.2457, -77.0322, -76.3002, -77.0929, -76.9168, -77.0596, -76.3262, -76.2383, -76.9931, -76.2594, -76.6433, -76.8727, -76.7852, -76.6102, -76.9271, -76.7521, -77.1667, -76.812, -76.6367, -77.1004, -77.0127, -76.2823, -77.0673, -76.9796, -76.3366, -76.3245, -76.9854, -76.8975, -77.1279, -76.9522, -76.509, -76.4212, -76.3335, -76.5636, -76.4757, -77.0283, -76.2961, -76.6394, -76.4475, -76.3596, -76.5901, -76.3808, -76.2928, -76.6114, -76.5234, -77.1976, -77.0225, -77.1645, -76.4353, -76.3479, -76.5771, -76.4021, -76.8649, -76.7773, -76.6023, -76.5107, -76.7496, -76.662, -76.8918, -76.8041, -76.6288, -77.0927, -76.2742, -76.8255, -76.7378, -76.5623, -76.7045, -76.9775, -76.8897, -77.1201, -76.9443, -76.8525, -76.7646, -76.6767, -76.5888, -77.0537, -76.2335, -77.0205, -76.288, -77.0263, -76.9383, -76.2049, -77.0812, -76.905, -76.8025, -77.1783, -77.0906, -77.003, -77.1452, -76.4152, -76.3277, -76.5571, -76.382, -76.8452, -76.5823, -76.4907, -76.7298, -76.6421, -76.5543, -76.8722, -76.7844, -76.6966, -76.6088, -76.2993, -76.6634, -76.8057, -76.7567, -77.0459, -76.9579, -76.2253, -76.6901, -76.6021, -76.5142, -76.8327, -76.6568, -76.5688, -76.2676, -76.5359, -76.4484, -76.6779, -76.8199, -76.6447, -77.1082, -76.2904, -76.8413, -76.7536, -76.5783, -76.9932, -76.9054, -77.1357, -76.96, -76.9268, -77.0693, -76.2498, -76.4889, -76.3132, -76.954, -76.866, -77.0968, -76.9207, -76.3889, -76.6195, -76.5315, -76.7308, -76.6818, -76.8239, -76.6487, -76.7907, -77.079, -76.9913, -76.3488, -76.8997, -76.7244, -77.1396, -76.9639, -77.1064, -76.2871, -77.0732, -76.2538, -77.04, -76.3083, -76.6514, -76.4596, -76.3718, -77.1007, -76.9247, -77.0674, -76.2465, -76.6235, -76.5355, -76.7661, -76.6781, -76.5021, -76.8183, -76.9602, -76.5731, -76.3981, -77.1237, -77.0361, -76.3066, -76.5067, -76.4736, -76.7031, -76.6155, -76.4243, -76.9307, -76.8879, -76.8002, -76.7125, -76.6248, -76.5331, -76.3578, -76.4999, -76.3839, -76.8485, -76.7606, -76.6727, -76.5848, -76.9912, -76.8153, -76.7273, -77.0166, -76.2839, -76.8914, -76.7328, -76.6995, -76.8317, -77.1198, -77.0322, -76.3025, -77.1744, -77.0867, -76.9991, -77.1413, -76.4112, -76.3236, -76.6991, -76.6115, -76.3447, -76.5836, -76.4958, -76.7259, -76.6381, -76.5503, -76.4202, -77.1473, -76.2953, -76.6594, -76.3799, -76.9872, -76.8993, -76.8113, -76.5435, -76.4556, -76.6861, -76.5981, -76.5102, -76.6898, -77.1529, -76.4232, -76.3358, -76.711, -76.6235, -76.8531, -76.7655, -76.5903, -76.9076, -76.7323, -77.081, -76.262, -77.0478, -76.3164, -77.0049, -76.9172, -76.65, -76.8801, -76.7923, -76.6168, -76.9658, -76.8778, -77.1085, -76.9325, -76.401, -77.042, -76.2212, -77.0087, -76.2757, -76.8502, -77.1392, -77.0517, -76.3228, -77.1937, -77.0186, -77.1607, -76.4313, -76.3438, -76.7189, -76.6314, -77.0945, -76.3649, -76.5159, -76.4283, -76.7457, -76.658, -76.9464, -76.6793, -76.5916, -76.8215, -76.5583, -76.4001, -77.0068, -76.8311, -76.7432, -76.9736, -76.8857, -76.2416, -76.706, -76.6181, -76.5303, -76.9071, -77.0498, -76.8581, -76.9676, -76.7915, -77.0224, -76.9343, -76.2008, -76.9524, -76.6858, -77.0614, -76.9738, -76.8862, -77.116, -77.0283, -76.2985, -77.1705, -77.0829, -76.9952, -76.4655, -76.5251, -76.4374, -76.3497, -76.5796, -76.4918, -76.9132, -77.1434, -76.3758, -76.8406, -76.6648, -76.4849, -76.397, -76.3091, -76.5395, -76.4516, -76.5651, -76.3901, -76.5319, -76.4444, -76.6739, -76.9621, -76.8744, -76.6952, -76.6075, -77.0225, -76.8469, -76.7591, -76.9893, -76.9015, -76.9229, -77.0752, -76.3425, -76.2546, -76.9833, -76.8074, -76.7194, -76.9501, -76.8621, -76.2172, -76.4182, -76.3849, -76.7986, -76.9407, -76.5531, -76.378, -77.1043, -77.0166, -76.2863, -76.4535, -76.4041, -76.4586, -76.3708, -76.5131, -76.4253, -76.3375, -76.8018, -76.7527, -76.5768, -76.3637, -76.8288, -76.6528, -76.9716, -76.8835, -76.7955, -76.9641, -76.5439, -76.4564, -77.1821, -77.0069, -76.4776, -76.7071, -76.6195, -76.8491, -76.7615, -76.5863, -76.9346, -77.0771, -76.2579, -77.0342, -76.8587, -76.771, -76.5039, -76.4162, -76.7338, -76.6461, -76.9951, -76.8192, -76.7313, -76.9618, -76.8739, -76.2294, -76.4303, -76.8953, -77.0381, -76.7035, -76.8463, -76.7017, -76.8435, -76.8104, -77.186, -77.0984, -77.0108, -76.9193, -76.7442, -76.6566, -76.3568, -76.4987, -77.1589, -76.3074, -76.6713, -76.8137, -76.5956, -76.5079, -77.0595, -76.9717, -77.1142, -76.4706, -76.3829, -76.392, -77.0869, -76.2668, -76.5556, -76.4677, -76.698, -76.6101, -76.5223, -76.6314, -76.7741, -76.4395, -76.3515, -76.5821, -76.8357, -76.6606, -76.5691, -76.3941, -76.857, -76.7694, -76.5943, -76.9115, -76.7363, -77.0536, -76.966, -76.8783, -77.0517, -76.3204, -76.4626, -76.3749, -77.1512, -76.9757, -76.884, -76.7962, -76.6208, -77.0264, -76.763, -77.1124, -76.9365, -77.0791, -76.2587, -76.6354, -76.5475, -77.0127, -76.2798, -76.4223, -76.3343, -76.9933, -77.1023, -76.373, -76.9446, -76.5239, -77.1628, -77.0751, -76.9874, -76.4575, -76.6872, -76.5996, -76.4081, -76.5171, -76.4293, -76.3416, -76.5716, -76.4838, -76.915, -76.6474, -76.7234, -76.3677, -76.9755, -76.8875, -76.7994, -77.0303, -76.9422, -76.209, -76.935, -76.76, -76.6725, -77.077, -76.9894, -76.9019, -77.1315, -77.0439, -76.3147, -76.5148, -76.9289, -77.1297, -76.4867, -76.3991, -76.5411, -76.3658, -76.8294, -76.4414, -77.1025, -76.2831, -76.7139, -76.6261, -76.5383, -76.8564, -76.6807, -76.5928, -76.501, -76.4132, -76.3254, -76.7899, -76.7408, -76.5648, -76.7075, -76.7622, -76.6741, -76.4981, -76.8169, -76.6408, -76.5528, -76.5559, -76.4685, -76.6977, -76.8396, -76.6646, -77.1276, -77.04, -76.3106, -76.8609, -76.7734, -76.5983, -76.3528, -76.925, -77.1551, -76.6673, -76.5371, -76.4494, -76.3618, -77.0888, -77.001, -76.2701, -77.0556, -76.9678, -76.3879, -77.1162, -76.9404, -76.497, -76.4091, -76.3213, -76.5515, -76.4637, -76.6275, -76.4688, -76.4354, -76.3474, -76.8278, -76.6527, -76.7947, -76.9368, -77.1374, -76.4947, -76.4071, -77.0459, -76.9582, -76.8705, -76.3407, -77.1103, -76.2912, -77.0439, -76.3123, -76.4545, -76.3668, -76.6554, -76.7978, -76.6061, -77.0713, -76.2505, -76.4809, -76.7701, -76.6821, -76.5062, -76.8248, -76.6488, -76.6155, -77.1061, -76.377, -76.5188, -76.7576, -76.6699, -77.1336, -76.4031, -76.3155, -76.6912, -76.6035, -76.8334, -76.5703, -76.5756, -76.4878, -76.7179, -76.6301, -76.5423, -76.9189, -77.0615, -76.7939, -76.87, -76.7447, -77.0342, -76.9461, -76.2131, -77.089, -77.0009, -76.9129, -76.8796, -76.585, -76.5519, -76.4644, -76.6937, -77.0692, -76.9816, -76.894, -76.715, -76.6274, -77.042, -76.7789, -77.0088, -76.9211, -76.4787, -76.391, -76.9425, -76.8547, -77.0849, -76.266, -77.0947, -76.275, -76.505, -76.9697, -76.8818, -76.4384, -76.3506, -76.4051, -76.3172, -77.0557, -76.3222, -76.2342, -76.4647, -76.2888, -76.4976, -76.4102, -76.7269, -76.6394, -76.8688, -76.7812, -76.6062, -77.0205, -76.9328, -76.666, -76.9542, -76.8665, -77.0966, -76.2782, -77.0146, -76.839, -76.7512, -76.9814, -76.8936, -76.4505, -76.3627, -76.4172, -76.3294, -77.0576, -76.2376, -76.4768, -76.301, -76.4435, -76.3555, -76.4101, -76.3768, -76.5267, -76.4936, -76.7229, -76.6354, -77.0497, -76.7868, -76.5199, -76.4323, -76.7204, -76.9503, -76.8626, -76.8682, -76.7804, -76.6926, -76.6048, -77.0107, -76.835, -76.7472, -77.0361, -76.3042, -76.4465, -76.3587, -76.9111, -77.0635, -76.3303, -76.2424, -76.4728, -76.2969, -76.997, -76.2635, -76.4061, -77.0808, -76.9058, -77.1353, -77.0478, -76.3187, -77.1898, -77.0147, -76.4856, -76.4363, -76.5451, -76.3699, -76.5119, -76.4454, -76.6753, -76.5876, -76.396, -76.8604, -76.7725, -76.6847, -76.5968, -77.0029, -76.8271, -76.7393, -76.5596, -76.4717, -76.9032, -76.7114, -76.8542, -76.8209, -76.6448, -76.5568, -76.9637, -76.8756, -76.7875, -76.8766, -76.7891, -76.6142, -76.9311, -76.756, -76.6685, -77.0731, -76.9855, -76.898, -76.3689, -76.3196, -76.7828, -77.0712, -76.9835, -77.1258, -76.4827, -76.3951, -76.6833, -76.3285, -77.1318, -76.9561, -77.0986, -76.279, -76.5676, -76.4798, -76.71, -76.6221, -76.5343, -76.4424, -76.3546, -76.6434, -76.786, -76.5941, -76.7368, -76.5608, -76.5274, -76.7582, -76.6701, -76.4941]
vals = [69, 69, 69, 66, 68, 65, 70, 68, 67, 67, 68, 67, 67, 67, 67, 67, 68, 66, 67, 67, 65, 66, 67, 66, 67, 66, 65, 67, 67, 65, 64, 66, 68, 69, 67, 70, 69, 70, 67, 70, 67, 69, 68, 67, 69, 67, 67, 69, 66, 68, 67, 68, 65, 67, 65, 66, 65, 67, 67, 65, 66, 64, 65, 64, 65, 64, 66, 66, 71, 68, 67, 69, 69, 68, 69, 68, 70, 65, 70, 68, 67, 67, 68, 69, 67, 67, 68, 66, 68, 65, 67, 66, 66, 66, 67, 67, 66, 67, 66, 66, 69, 69, 68, 70, 68, 66, 69, 69, 69, 66, 67, 66, 65, 67, 67, 64, 66, 66, 68, 67, 67, 67, 65, 64, 66, 67, 67, 66, 64, 65, 65, 65, 69, 69, 67, 68, 68, 67, 69, 69, 67, 68, 68, 69, 67, 67, 67, 68, 68, 66, 65, 65, 65, 64, 65, 66, 64, 66, 65, 64, 66, 66, 71, 69, 69, 69, 68, 68, 67, 69, 67, 67, 67, 68, 67, 66, 65, 67, 67, 65, 67, 64, 65, 64, 65, 66, 65, 63, 66, 65, 64, 66, 65, 65, 66, 66, 69, 67, 69, 67, 67, 70, 69, 70, 67, 69, 69, 67, 69, 68, 66, 69, 65, 66, 67, 68, 67, 68, 65, 67, 65, 67, 67, 67, 67, 66, 65, 62, 65, 64, 64, 66, 66, 64, 64, 66, 68, 68, 67, 69, 66, 65, 69, 68, 68, 69, 68, 68, 68, 67, 67, 67, 68, 67, 66, 67, 67, 67, 65, 66, 65, 67, 67, 66, 67, 67, 67, 65, 68, 68, 69, 67, 69, 68, 67, 66, 66, 69, 67, 67, 66, 67, 67, 65, 65, 66, 64, 66, 67, 65, 66, 65, 66, 66, 68, 68, 67, 68, 66, 68, 66, 68, 68, 67, 65, 68, 66, 65, 65, 63, 65, 65, 67, 65, 65, 65, 66, 65, 64, 67, 66, 67, 67, 66, 70, 67, 70, 69, 69, 67, 65, 70, 68, 69, 68, 66, 67, 68, 67, 69, 68, 68, 66, 67, 64, 67, 67, 67, 66, 65, 67, 66, 65, 64, 66, 66, 66, 69, 69, 68, 65, 68, 68, 68, 68, 68, 65, 68, 69, 67, 67, 66, 67, 67, 66, 66, 66, 65, 67, 65, 65, 67, 67, 66, 65, 67, 67, 66, 67, 69, 67, 67, 68, 69, 69, 67, 68, 69, 68, 66, 64, 67, 64, 68, 68, 68, 68, 67, 68, 66, 67, 65, 66, 65, 65, 64, 65, 65, 66, 69, 70, 66, 69, 67, 69, 66, 66, 68, 69, 69, 67, 68, 66, 67, 69, 68, 68, 67, 67, 68, 67, 65, 67, 67, 67, 67, 64, 67, 67, 65, 67, 65, 66, 65, 66, 64, 64, 64, 68, 68, 66, 69, 70, 69, 68, 64, 68, 68, 68, 67, 68, 67, 65, 67, 66, 68, 65, 64, 67, 67, 66, 65, 65, 66, 65, 68, 69, 70, 68, 69, 68, 69, 68, 69, 67, 67, 68, 67, 68, 67, 65, 65, 66, 65, 68, 67, 66, 67, 64, 66, 65, 66, 68, 69, 68, 68, 66, 67, 66, 66, 64, 65, 64, 67, 65, 67, 67, 66, 64, 66, 67, 65, 66, 66, 69, 70, 68, 68, 67, 69, 69, 67, 68, 66, 68, 67, 66, 64, 68, 68, 68, 68, 66, 68, 68, 65, 67, 68, 66, 67, 66, 66, 66, 65, 67, 64, 68, 70, 69, 69, 69, 68, 69, 67, 68, 65, 69, 68, 67, 68, 67, 68, 68, 67, 68, 67, 67, 66, 66, 65, 66, 65, 64, 66, 67, 66, 66, 67, 66, 66, 66, 69, 67, 67, 66, 69, 68, 67, 70, 69, 65, 68, 70, 67, 64, 65, 65, 67, 68, 68, 67, 68, 67, 68, 65, 67, 65, 63, 67, 66, 65, 66, 65, 64, 67, 69, 66, 69, 69, 68, 68, 67, 67, 69, 68, 66, 66, 67, 64, 66, 64, 67, 67, 66, 65, 65, 66, 66, 64, 66, 67, 69, 69, 68, 70, 67, 70, 69, 68, 66, 69, 68, 66, 68, 66, 68, 67, 68, 67, 65, 64, 67, 66, 65, 67, 67, 66, 66, 63, 64, 67, 67, 66, 67, 66, 67, 65, 64, 67, 66, 70, 67, 68, 70, 66, 69, 66, 67, 69, 67, 67, 65, 69, 67, 68, 69, 66, 67, 66, 68, 65, 67, 67, 64, 64, 67, 66, 63, 64, 66, 65, 67, 66, 66, 66, 68, 68, 66, 68, 69, 68, 67, 67, 68, 69, 67, 66, 65, 67, 65, 64, 65, 67, 67, 66, 65, 65, 66, 67, 67, 66, 66, 67, 66, 69, 67, 68, 67, 69, 68, 67, 67, 68, 69, 68, 68, 66, 64, 67, 66, 66, 67, 65, 67, 67, 67, 65, 66, 64, 64, 65, 66, 66, 68, 70, 68, 68, 68, 68, 71, 68, 69, 67, 66, 67, 68, 67, 66, 68, 68, 65, 65, 65, 64, 65, 66, 67, 63, 64, 65, 66, 64, 65, 67, 66, 66, 68, 67, 69, 67, 71, 68, 69, 66, 68, 69, 68, 69, 67, 67, 67, 67, 67, 66, 67, 66, 64, 64, 63, 65, 63, 65, 65, 66, 65, 65, 65, 70, 68, 68, 68, 65, 66, 69, 67, 68, 68, 68, 67, 67, 68, 66, 65, 67, 67, 65, 64, 65, 64, 67, 65, 66, 64, 65, 64, 65, 66, 65, 70, 70, 69, 70, 66, 69, 67, 67, 67, 68, 66, 68, 67, 68, 67, 66, 67, 68, 67, 66, 65, 67, 67, 65, 65, 67, 67, 66, 66, 67, 66, 64, 64, 66, 71, 70, 69, 69, 66, 67, 68, 67, 71, 69, 68, 66, 68, 67, 65, 67, 66, 68, 65, 65, 67, 65, 64, 66, 65, 67, 66, 64, 63, 63, 66, 67, 66, 67, 66, 66, 66, 66, 65]

def lambda_handler(event, context):
  fig, ax = plt.subplots()
  cax = fig.add_axes([0.77, 0.12, 0.02, 0.75])
  ax.set_title(desc)
  
  m = Basemap(
    resolution='h',
    projection='lcc',
    rsphere=6371200.0,
    lon_0=265.0,
    lat_0=25.0,
    lat_1=25.0,
    lat_2=25.0,
    llcrnrlon=min(lons) - 0.05,
    llcrnrlat=min(lats),
    urcrnrlon=max(lons) + 0.05,
    urcrnrlat=max(lats),
    ax=ax,
  )
  
  m.fillcontinents(color='white', lake_color='aqua')
  m.drawcoastlines()
  m.drawrivers(color='blue')
  
  x, y = m(lons, lats)
  levels = list(np.linspace(min(vals), max(vals), num=25))
  contours = ax.tricontourf(x, y, vals, levels=levels, cmap=plt.cm.gnuplot2, alpha=0.5, antialiased=True, zorder=20)
  fig.colorbar(contours, cax=cax, orientation='vertical', format='%.1f')
  
  digits = []
  for i in range(len(vals)):
    px, py = m(lons[i], lats[i])
    digit = ax.text(px, py, vals[i], fontsize=3, ha='center', va='center')
    digits.append(digit)
  
  plt.savefig('/tmp/test.png', bbox_inches='tight', dpi=300)
  
  bucket.upload_file(
    Filename='/tmp/test.png',
    Key='test.png',
    ExtraArgs=dict(
      ACL='public-read',
      #CacheControl=
      ContentType='image/png',
    ),
  )
  
  remove('/tmp/test.png')
  