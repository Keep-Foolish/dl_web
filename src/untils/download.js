import axios from 'axios';
import JSZip from 'jszip';
import { load } from './loading';


// 保存两张图片和 JSON 数据到 ZIP 文件
export const saveFilesAsZip = async (imageUrl1, imageUrl2, lodging_area, folderName) => {
  load.show("正在请求资源...");
  try {
    // 创建 ZIP 实例
    const zip = new JSZip();

    // 1. 保存 JSON 文件
    const jsonFileName = 'lodging_area.json';
    const jsonBlob = new Blob([JSON.stringify(lodging_area, null, 2)], { type: 'application/json' });
    zip.file(jsonFileName, jsonBlob);

    // 2. 下载并保存第一个图片（原图）
    const response1 = await axios.get(imageUrl1, { responseType: 'arraybuffer' });
    const imageBlob1 = new Blob([response1.data], { type: 'image/png' }); // 假设为 JPEG 格式
    const imageFileName1 = 'original_image.png';
    zip.file(imageFileName1, imageBlob1);

    // 3. 下载并保存第二个图片（标注图像）
    const response2 = await axios.get(imageUrl2, { responseType: 'arraybuffer' });
    const imageBlob2 = new Blob([response2.data], { type: 'image/png' }); // 假设为 JPEG 格式
    const imageFileName2 = 'annotated_image.png';
    zip.file(imageFileName2, imageBlob2);

    // 4. 生成 ZIP 文件并提供下载
    const zipBlob = await zip.generateAsync({ type: 'blob' });

    // 创建下载链接
    const zipUrl = URL.createObjectURL(zipBlob);
    const zipLink = document.createElement('a');
    zipLink.href = zipUrl;
    zipLink.download = `${folderName.split('.')[0]}.zip`; // 文件夹名称作为 ZIP 文件名
    zipLink.click();
    load.hide()
  } catch (error) {
    console.error('保存失败:', error);
  }
};
