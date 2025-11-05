<template>
  <div class="about-page">
    <div class="about-card">
      <h2>关于像素画色号标注工具</h2>
      <p>这是一个专为像素画爱好者设计的工具，可以帮助你快速分析像素画中的颜色信息，并为每个颜色生成唯一的色号标注。</p>
      
      <div class="features">
        <h3>主要功能</h3>
        <ul>
          <li><strong>图片上传：</strong>支持拖放或点击上传像素画图片</li>
          <li><strong>颜色分析：</strong>自动分析图片中的所有颜色并统计每种颜色的使用频率</li>
          <li><strong>色号标注：</strong>在原图上为每种颜色添加唯一的色号标记，方便查看和使用</li>
          <li><strong>响应式设计：</strong>适配各种设备屏幕，在手机、平板和电脑上都能正常使用</li>
        </ul>
      </div>
      
      <div class="how-to-use">
        <h3>使用方法</h3>
        <ol>
          <li>点击或拖放上传一张像素画图片</li>
          <li>系统会自动分析图片中的颜色并进行统计</li>
          <li>查看处理后的图片，每个颜色都会有对应的色号标记</li>
          <li>在下方的颜色统计列表中，可以查看每种颜色的色值和使用次数</li>
        </ol>
      </div>
    </div>
    
    <div class="about-card">
      <h3>关于技术</h3>
      <p>这个工具是基于现代Web技术开发的PWA应用，可以安装到本地使用，支持离线功能。</p>
      <ul>
        <li>前端框架：Vue.js 3 + TypeScript</li>
        <li>构建工具：Vite</li>
        <li>样式：原生CSS</li>
        <li>图像处理：Canvas API</li>
      </ul>
    </div>
    
    <div class="about-card">
      <h3>更新日志</h3>
      <div class="update-item">
        <h4>v1.0.0 (2024-03-XX)</h4>
        <ul>
          <li>初始版本发布</li>
          <li>实现基本的图片上传和颜色分析功能</li>
          <li>添加色号标注功能</li>
          <li>支持响应式设计</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 关于页面的逻辑
</script>

<style scoped>
.about-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.about-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.about-card h2 {
  margin-top: 0;
  color: #333;
  font-size: 1.8rem;
  border-bottom: 2px solid #42b983;
  padding-bottom: 0.5rem;
}

.about-card h3 {
  color: #42b983;
  margin-top: 1.5rem;
  font-size: 1.4rem;
}

.about-card p {
  line-height: 1.6;
  color: #666;
}

.features, .how-to-use {
  margin-top: 1.5rem;
}

.features ul, .how-to-use ol {
  padding-left: 1.5rem;
}

.features li, .how-to-use li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.update-item {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.update-item:last-child {
  border-bottom: none;
}

.update-item h4 {
  color: #333;
  margin-bottom: 0.5rem;
}

.update-item ul {
  padding-left: 1.5rem;
}

.update-item li {
  margin-bottom: 0.3rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .about-card {
    padding: 1.5rem;
  }
  
  .about-card h2 {
    font-size: 1.5rem;
  }
  
  .about-card h3 {
    font-size: 1.2rem;
  }
}
</style>