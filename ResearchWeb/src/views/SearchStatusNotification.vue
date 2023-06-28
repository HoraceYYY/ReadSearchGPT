<template>
  <div v-if="visible" :class="['search-status-notification', notificationClass]">
    <div class="notification-content">
      <span class="message-icon" :class="{ 'icon-loading': !completed, 'icon-checkmark': completed }"></span>
      <span>{{ message }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    message: {
      type: String,
      required: true,
    },
    completed: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    notificationClass() {
      return this.completed ? 'completed' : 'ongoing';
    },
  },
};
</script>

<style scoped>
.search-status-notification {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9999;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  color: #ffffff;
  transition: opacity 0.3s ease;
}

.ongoing {
  background-color: #f8b500; /* Ongoing status background color */
}

.completed {
  background-color: #00a651; /* Completed status background color */
}

.notification-content {
  display: flex;
  align-items: center;
  justify-content: center;
}
.message-icon {
  margin-right: 8px;
}

.icon-loading {
  border: 2px solid #fff;
  border-top: 2px #2c2c2c;
  border-radius: 50%;
  width: 12px;
  height: 12px;
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.icon-checkmark::before {
  content: "✔";
}
</style>
