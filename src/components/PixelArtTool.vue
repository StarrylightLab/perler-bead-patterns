<template>
  <div class="pixel-art-tool">
    <div class="upload-section">
      <h2>上传像素画</h2>
      <div class="upload-area" @dragover.prevent @drop="handleDrop">
        <input
          type="file"
          id="file-upload"
          accept="image/*"
          @change="handleFileChange"
        />
        <label for="file-upload" class="upload-label">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <p>拖放图片到此处，或点击选择图片</p>
        </label>
      </div>
    </div>

    <div class="preview-section" v-if="imageData">
      <div class="original-image">
        <h3>原图</h3>
        <img :src="imageData" alt="上传的像素画" :style="{ maxWidth: '100%', maxHeight: '500px' }" />
      </div>
      
      <div class="processed-image">
        <h3>处理后的图像（带色号）</h3>
        <canvas ref="canvas" :width="canvasWidth" :height="canvasHeight"></canvas>
      </div>
    </div>

    <div class="color-stats" v-if="colors.length > 0">
      <h3>颜色统计</h3>
      <div class="color-grid">
        <div v-for="(color, index) in colors" :key="index" class="color-item">
          <div 
            class="color-swatch" 
            :style="{ backgroundColor: color.hex }"
            :title="`${color.hex} (${color.count}个像素)`"
          ></div>
          <span class="color-code">#{{ color.hex }}</span>
          <span class="color-count">({{ color.count }})</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface ColorInfo {
  hex: string
  count: number
}

const fileInput = ref<HTMLInputElement>()
const imageData = ref<string | null>(null)
const canvasWidth = ref(0)
const canvasHeight = ref(0)
const colors = ref<ColorInfo[]>([])
const canvas = ref<HTMLCanvasElement>()

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    processImage(target.files[0])
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  if (event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0]) {
    processImage(event.dataTransfer.files[0])
  }
}

const processImage = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    if (e.target && typeof e.target.result === 'string') {
      imageData.value = e.target.result
      analyzeImage(e.target.result)
    }
  }
  reader.readAsDataURL(file)
}

const analyzeImage = (imageSrc: string) => {
  const img = new Image()
  img.onload = () => {
    // 设置画布尺寸
    canvasWidth.value = img.width
    canvasHeight.value = img.height
    
    const ctx = canvas.value?.getContext('2d')
    if (!ctx) return
    
    // 绘制图像到画布
    ctx.drawImage(img, 0, 0)
    
    // 获取图像数据
    const imageData = ctx.getImageData(0, 0, canvasWidth.value, canvasHeight.value)
    const data = imageData.data
    
    // 统计颜色
    const colorMap = new Map<string, number>()
    
    for (let i = 0; i < data.length; i += 4) {
      const r = data[i]
      const g = data[i + 1]
      const b = data[i + 2]
      const a = data[i + 3]
      
      // 忽略透明像素
      if (a === 0) continue
      
      // 将RGB转换为十六进制
      const hex = rgbToHex(r, g, b)
      
      // 更新颜色计数
      colorMap.set(hex, (colorMap.get(hex) || 0) + 1)
    }
    
    // 转换为数组并排序
    colors.value = Array.from(colorMap.entries())
      .map(([hex, count]) => ({ hex, count }))
      .sort((a, b) => b.count - a.count)
    
    // 在图像上标注色号
    labelColorsOnCanvas(ctx, colorMap, img.width, img.height)
  }
  img.src = imageSrc
}

const rgbToHex = (r: number, g: number, b: number): string => {
  return `${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase()
}

const labelColorsOnCanvas = (ctx: CanvasRenderingContext2D, colorMap: Map<string, number>, width: number, height: number) => {
  // 首先绘制原始图像
  const img = new Image()
  img.onload = () => {
    ctx.drawImage(img, 0, 0)
    
    // 为每种颜色创建映射，获取其在统计列表中的索引
    const colorIndexMap = new Map<string, number>()
    colors.value.forEach((color, index) => {
      colorIndexMap.set(color.hex, index + 1) // +1 让色号从1开始
    })
    
    // 遍历每个像素，在左上角添加色号标记
    const cellSize = 10 // 标记尺寸
    const gridSize = Math.max(1, Math.floor(Math.min(width, height) / 100)) // 每隔多少像素标记一次
    
    for (let y = 0; y < height; y += gridSize) {
      for (let x = 0; x < width; x += gridSize) {
        const pixelData = ctx.getImageData(x, y, 1, 1).data
        const r = pixelData[0]
        const g = pixelData[1]
        const b = pixelData[2]
        const a = pixelData[3]
        
        if (a === 0) continue
        
        const hex = rgbToHex(r, g, b)
        const index = colorIndexMap.get(hex)
        
        if (index !== undefined) {
          // 绘制标记背景
          ctx.fillStyle = 'rgba(255, 255, 255, 0.7)'
          ctx.fillRect(x, y, cellSize, cellSize)
          
          // 绘制标记边框
          ctx.strokeStyle = '#000'
          ctx.lineWidth = 1
          ctx.strokeRect(x, y, cellSize, cellSize)
          
          // 绘制色号文字
          ctx.fillStyle = '#000'
          ctx.font = '8px Arial'
          ctx.textAlign = 'center'
          ctx.textBaseline = 'middle'
          ctx.fillText(index.toString(), x + cellSize / 2, y + cellSize / 2)
        }
      }
    }
  }
  img.src = imageData.value || ''
}

// 为了支持PWA，确保图像在画布上正确渲染
onMounted(() => {
  if (imageData.value) {
    analyzeImage(imageData.value)
  }
})
</script>

<style scoped>
.pixel-art-tool {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.upload-section {
  text-align: center;
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 8px;
  padding: 2rem;
  transition: all 0.3s;
}

.upload-area:hover {
  border-color: #42b983;
  background-color: #f0f9f5;
}

#file-upload {
  display: none;
}

.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  color: #666;
}

.upload-label:hover {
  color: #42b983;
}

.upload-label svg {
  margin-bottom: 1rem;
}

.preview-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.original-image, .processed-image {
  text-align: center;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.original-image h3, .processed-image h3 {
  margin-top: 0;
  color: #333;
}

canvas {
  max-width: 100%;
  border: 1px solid #ddd;
  image-rendering: pixelated;
}

.color-stats {
  margin-top: 2rem;
}

.color-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.color-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.color-swatch {
  width: 30px;
  height: 30px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.color-code {
  font-family: monospace;
  font-weight: bold;
  color: #333;
}

.color-count {
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .preview-section {
    grid-template-columns: 1fr;
  }
  
  .color-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>