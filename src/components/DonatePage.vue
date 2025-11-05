<template>
  <div class="donate-page">
    <div class="donate-card">
      <h2>支持我们</h2>
      <p>如果你喜欢这个工具，并觉得它对你有所帮助，欢迎通过以下方式支持我们的开发工作。你的支持将帮助我们持续改进和更新这个工具。</p>
      
      <div class="donate-methods">
        <div class="donate-item">
          <div class="donate-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="6" width="20" height="12" rx="2"/>
              <line x1="2" y1="10" x2="22" y2="10"/>
              <path d="M6 12h.01M10 12h.01M14 12h.01M18 12h.01"/>
            </svg>
          </div>
          <div class="donate-info">
            <h3>微信支付</h3>
            <div class="qr-code">
              <img src="/wechat-qr.png" alt="微信支付二维码" v-if="false" />
              <div class="placeholder-qr" v-else>
                <svg width="150" height="150" viewBox="0 0 150 150" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="0" y="0" width="150" height="150" fill="white" stroke="#ddd"/>
                  <rect x="20" y="20" width="40" height="40" fill="#07C160"/>
                  <rect x="90" y="20" width="40" height="40" fill="#07C160"/>
                  <rect x="20" y="90" width="40" height="40" fill="#07C160"/>
                  <rect x="90" y="90" width="40" height="40" fill="#07C160"/>
                  <rect x="55" y="55" width="40" height="40" fill="#07C160"/>
                  <rect x="20" y="55" width="40" height="40" fill="white"/>
                  <rect x="90" y="55" width="40" height="40" fill="white"/>
                  <rect x="55" y="20" width="40" height="40" fill="white"/>
                  <rect x="55" y="90" width="40" height="40" fill="white"/>
                  <circle cx="75" cy="75" r="10" fill="#07C160"/>
                </svg>
              </div>
              <p>扫描二维码支持我们</p>
            </div>
          </div>
        </div>
        
        <div class="donate-item">
          <div class="donate-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="6" width="20" height="12" rx="2"/>
              <line x1="2" y1="10" x2="22" y2="10"/>
              <path d="M6 12h.01M10 12h.01M14 12h.01M18 12h.01"/>
            </svg>
          </div>
          <div class="donate-info">
            <h3>支付宝</h3>
            <div class="qr-code">
              <img src="/alipay-qr.png" alt="支付宝二维码" v-if="false" />
              <div class="placeholder-qr" v-else>
                <svg width="150" height="150" viewBox="0 0 150 150" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="0" y="0" width="150" height="150" fill="white" stroke="#ddd"/>
                  <rect x="20" y="20" width="40" height="40" fill="#1677FF"/>
                  <rect x="90" y="20" width="40" height="40" fill="#1677FF"/>
                  <rect x="20" y="90" width="40" height="40" fill="#1677FF"/>
                  <rect x="90" y="90" width="40" height="40" fill="#1677FF"/>
                  <rect x="55" y="55" width="40" height="40" fill="#1677FF"/>
                  <rect x="20" y="55" width="40" height="40" fill="white"/>
                  <rect x="90" y="55" width="40" height="40" fill="white"/>
                  <rect x="55" y="20" width="40" height="40" fill="white"/>
                  <rect x="55" y="90" width="40" height="40" fill="white"/>
                  <circle cx="75" cy="75" r="10" fill="#1677FF"/>
                </svg>
              </div>
              <p>扫描二维码支持我们</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="donation-message">
        <h3>捐赠名单</h3>
        <p>感谢以下用户的支持（按时间顺序）：</p>
        <ul class="donor-list">
          <li class="donor-item" v-for="(donor, index) in donors" :key="index">
            <span class="donor-name">{{ donor.name }}</span>
            <span class="donor-amount">{{ donor.amount }}</span>
            <span class="donor-date">{{ donor.date }}</span>
          </li>
        </ul>
        <p v-if="donors.length === 0" class="no-donors">暂无捐赠记录，成为第一个支持我们的人吧！</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Donor {
  name: string
  amount: string
  date: string
}

const donors: Donor[] = [
  // 这里可以添加真实的捐赠记录
  // 示例：{ name: '匿名用户', amount: '¥20', date: '2024-03-15' }
]
</script>

<style scoped>
.donate-page {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.donate-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.donate-card h2 {
  margin-top: 0;
  color: #333;
  font-size: 1.8rem;
  border-bottom: 2px solid #42b983;
  padding-bottom: 0.5rem;
}

.donate-card h3 {
  color: #42b983;
  margin-top: 1.5rem;
  font-size: 1.4rem;
}

.donate-card p {
  line-height: 1.6;
  color: #666;
}

.donate-methods {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.donate-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 8px;
  transition: all 0.3s;
}

.donate-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.donate-icon {
  margin-bottom: 1rem;
  color: #42b983;
}

.donate-info {
  text-align: center;
}

.qr-code {
  margin-top: 1rem;
}

.qr-code img {
  max-width: 150px;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.placeholder-qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.qr-code p {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #999;
}

.donation-message {
  margin-top: 2rem;
}

.donor-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.donor-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1rem;
  border-bottom: 1px solid #eee;
  transition: background-color 0.3s;
}

.donor-item:hover {
  background-color: #f9f9f9;
}

.donor-item:last-child {
  border-bottom: none;
}

.donor-name {
  font-weight: 500;
  color: #333;
}

.donor-amount {
  color: #e74c3c;
  font-weight: 600;
}

.donor-date {
  color: #999;
  font-size: 0.9rem;
}

.no-donors {
  text-align: center;
  color: #999;
  font-style: italic;
  padding: 2rem;
}

@media (max-width: 768px) {
  .donate-card {
    padding: 1.5rem;
  }
  
  .donate-card h2 {
    font-size: 1.5rem;
  }
  
  .donate-card h3 {
    font-size: 1.2rem;
  }
  
  .donate-methods {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .donor-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>