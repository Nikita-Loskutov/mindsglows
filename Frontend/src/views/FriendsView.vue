<script setup>
    import { ref, onMounted } from 'vue'

    const apiServ = 'https://4e27-57-129-20-194.ngrok-free.app'
    const userId = document.querySelector('meta[name="user-id"]')?.content || ''

    const copySuccess = ref(false)
    const referrals = ref([])

    const referralLink = `${apiServ}/invite?referrer_id=${userId}`

    const copyReferralLink = async () => {
    try {
        await navigator.clipboard.writeText(referralLink)
        copySuccess.value = true
        setTimeout(() => {
        copySuccess.value = false
        }, 2000)
    } catch (err) {
        console.error('Failed to copy referral link: ', err)
    }
    }

    const shareReferralLink = () => {
    const message = `🎉 Привет! Я приглашаю тебя в MMM Coin. Получи бонусы и начни зарабатывать! 💰\n\n👉 Присоединяйся\n5000 монет в качестве подарка\n25000 монет, если у тебя есть Telegram Premium`

    if (typeof Telegram !== 'undefined' && Telegram.WebApp) {
        Telegram.WebApp.openTelegramLink(
        `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=${encodeURIComponent(message)}`
        )
    } else if (navigator.userAgent.includes('Telegram')) {
        window.location.href = `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=${encodeURIComponent(message)}`
    } else if (navigator.share) {
        navigator
        .share({
            title: 'Приглашение в MMM Coin',
            text: message,
            url: referralLink,
        })
        .catch((err) => console.error('Ошибка при отправке ссылки:', err))
    } else {
        alert('Telegram WebApp не поддерживается. Отправьте ссылку вручную.')
    }
    }

    const fetchReferrals = async () => {
    try {
        const res = await fetch(`/invited_friends?user_id=${userId}`)
        const data = await res.json()
        if (res.ok && data.success) {
        referrals.value = data.referrals
        } else {
        console.error('Failed to load referrals:', data.error)
        }
    } catch (err) {
        console.error('Error fetching referrals:', err)
    }
    }

    onMounted(fetchReferrals)
</script>

<template>
  <div class="container">
    <div id="copy-notification" v-show="copySuccess">Text copied!</div>
    
    <div class="head">
      <h1>Пригласите друзей!</h1>
      <p>Вы и ваш друг получите бонусы</p>
    </div>

    <div class="new">
      <h3>Пригласить друга</h3>
      <p><span style="color:#bd9400">● +5000</span> монет для вас и вашего друга</p>
    </div>

    <div class="new">
      <h3>Пригласить друга с Telegram Premium</h3>
      <p><span style="color:#bd9400">● +25000</span> монет для вас и вашего друга</p>
    </div>

    <div class="referals">
      <h2>Список ваших друзей ({{ referrals.length }})</h2>
      <div id="referrals-list">
        <div v-for="ref in referrals" :key="ref.id" class="refblock">
          <img src="/src/assets/user.png" />
          <h3>{{ ref.name }}</h3>
        </div>
      </div>
    </div>

    <div class="invite">
      <button class="inv" @click="shareReferralLink">Пригласить друга</button>
      <button class="copy" @click="copyReferralLink">☐</button>
    </div>
  </div>
</template>

<style scoped>
    .container {
        display:block;
        margin:0 auto;
        justify-content: center;
        align-items: center;
        height:78%;
        background: #1e1e1e;
        border-radius: 30px 30px 30px 30px;
        padding: 20px;
        box-shadow: 0px 0px 8px #6366F1;
        text-align: center;
        overflow-y: auto; 
        overflow-x: hidden;
    }

    .head h1{
        margin-top:5px;

    }

    h3{
        margin:0;
        padding:0;
    }

    .new {
        display:block;
        margin:0 auto;
        margin-bottom: 15px;
        padding:15px;
        background: #1e1e1e;
        border-radius: 40px;
        box-shadow: 0px 0px 8px #6366F1;
        justify-content: center;
        align-items: center;
    }

    .referals h2 {
        display:flex;
        font-size:16px;
        margin:0;
        margin-top:50px;
    }


    .refblock {
        display:flex;
        margin:0;
        margin-top: 15px;
        margin-bottom: 15px;
        padding:15px;
        background: #1e1e1e;
        border-radius: 40px;
        box-shadow: 0px 0px 5px #6366F1;
    }

    .refblock img {
        width:25px;
        height:25px;
        padding:5px;
    }

    .refblock h3{
        display:flex;
        margin:0;
        padding:0;
        font-size:15px;
        align-items:center;
    }

    .invite {
        display:flex;
        justify-content:center;
        align-items:center;
        padding-bottom:80px;
    }

    .inv {
        font-size: 25px;
        background-color:#773ffa;
        border: none;
        border-radius:10px;
        padding:10px;
        justify-content:center;
        align-items:center;
        animation: pulse 2s infinite;
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.5);
    }

    .copy {
        display:flex;
        font-size: 25px;
        background-color:#773ffa;
        border: none;
        border-radius:10px;
        padding-top:8px;
        padding-bottom:8px;
        padding-left:15px;
        padding-right:15px;
        justify-content:center;
        align-items:center;
        margin-left:15px;
        box-shadow: 0 0 12px rgba(139, 92, 246, 0.5);

    }
    @keyframes pulse {
        0%, 100% {
            transform: scale(1); 
        }
        50% {
            transform: scale(1.05); 
        }
    }

    #copy-notification {
        display: block;
        position: fixed;
        bottom: 150%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333333de;
        color: white;
        padding: 10px;
        border: 2px solid black;
        border-radius: 15px;
        z-index: 1000;
        transition: all 1s;
    }
</style>
