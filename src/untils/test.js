import GeoTIFF from 'geotiff';

// 计算空间分辨率（每像素的地面面积）
async function calculateSpatialResolution(tifFile) {
    // 使用 fromUrl 来读取 tif 文件
    const tiff = await GeoTIFF.fromUrl(tifFile); 
    const image = await tiff.getImage();
    
    const transform = image.getGeoTransform();
    const crs = await image.getCRS();

    console.log("图像坐标参考系统（CRS）:", crs);

    // 图像尺寸
    const width = image.getWidth();
    const height = image.getHeight();

    // 获取图像的空间变换矩阵（geotransform）
    // [pixelWidth, rotation1, rotation2, pixelHeight, rotation3, rotation4]
    const pixelWidth = transform[0];   // 经度方向的像素大小
    const pixelHeight = transform[3];  // 纬度方向的像素大小（负值）

    // 获取图像中心的地理坐标
    const centerX = transform[0] + (width / 2) * transform[1]; // 中心X坐标
    const centerY = transform[3] + (height / 2) * transform[4]; // 中心Y坐标

    console.log(`图像中心地理坐标: (${centerX}, ${centerY})`);

    // 使用纬度计算每个像素的实际面积
    const latitudeRad = Math.radians(centerY);

    // 经度方向的每像素尺寸
    const pixelWidthInMeters = Math.abs(pixelWidth) * 111320 * Math.cos(latitudeRad);
    
    // 纬度方向的每像素尺寸
    const pixelHeightInMeters = Math.abs(pixelHeight) * 111320;

    // 每个像素的面积（平方米）
    const pixelArea = pixelWidthInMeters * pixelHeightInMeters;

    console.log(`每像素面积：${pixelArea.toFixed(4)} 平方米`);
    
    return pixelArea;
}
    


// 为了计算弧度
Math.radians = function(degrees) {
    return degrees * Math.PI / 180;
};
// 使用示例（提供路径到 GeoTIFF 文件）
const tifFile = 'C:/Users/zhangwei/Desktop/小麦倒伏数据/tif/20210531-field2.tif';
calculateSpatialResolution(tifFile);
