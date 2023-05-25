<script>
export default {
  data() {
    return {
      feedback: "",
      successMessage: "",
      displayMessage: false,
      errorMessage: "",
      displayError: false,
      buttonText: "Send"
    };
  },
  computed: {
    wordCount() {
      return this.feedback.length;
    }
  },
  methods: {
    async sendFeedback() {
        if (!this.feedback.trim()) {
          this.errorMessage = "Please enter your feedback before sending.";
          this.displayError = true;
          setTimeout(() => {
          this.displayError = false;
          this.errorMessage = "";
        }, 3000);
          return;
        }
        try {
        const url = "https://readsearch-hauf6ju5bq-uc.a.run.app/feedback";  // replace with your API endpoint
        const data = {
          feedback: this.feedback
        };

        this.displayMessage = true;
        this.buttonText = "Sending...";

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        });

        if (response.ok) {
          this.successMessage = "Thank you for your feedback!";
          this.feedback = "";
          this.buttonText = "Send";
        } else {
          throw new Error('Error sending feedback');
        }

        setTimeout(() => {
          this.displayMessage = false;
          this.successMessage = "";
        }, 3000);
      } catch (error) {
        this.errorMessage = "There was an error sending your feedback.";
        this.displayError = true;
        this.buttonText = "Send";
        setTimeout(() => {
          this.displayError = false;
          this.errorMessage = "";
        }, 3000);
      }
    }
  }
};
</script>

<template>
  <div class="form-container">
    <form @submit.prevent="sendFeedback">
      <div class="input-group">
        <label for="feedback" class="input-label">Tell us about your experience of the product or you new features you would like to see:</label>
        <textarea id="feedback" v-model="feedback" class="text-input" placeholder="Enter your feedback here..." maxlength="1500" rows="8" />
        <p v-if="wordCount > 1500" class="word-count-warning">Please limit your feedback to 1500 words</p>
      </div>
      <div class="button-container">
        <button type="submit" class="send-button" :disabled="wordCount > 1500">{{ this.buttonText }}</button>
      </div>
      <p v-if="displayMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="displayError" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.input-group {
  width: 900px;
  margin-bottom: 20px;
  font-family: Arial, sans-serif;
  font-size: 20px;
}

.input-label {
  font-weight: bold;
  margin-bottom: 10px;
}

.text-input {
  width: 96%;
  margin: 10px 0;
  font-style: italic;
  font-family: Arial, sans-serif;
  font-size: 18px;
  padding: 10px;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 120px;
  margin-top: 40px;
}

.send-button {
  border: 2px solid #0c952c;
  border-radius: 8px;
  background-color: #ffffff;
  color: #0c952c;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

.send-button:hover {
  background-color: #0c952c;
  color: #ffffff;
}

.word-count-warning, .success-message {
  color: red;
  text-align: center;
}

.success-message {
  color: green;
}
.error-message {
  color: red;
  text-align: center;
}
</style>
