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
        const url = "https://readsearchapi.ashymoss-b9207c1e.westus.azurecontainerapps.io/feedback";  // replace with your API endpoint
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
  <div class="container">
    <form @submit.prevent="sendFeedback">
      <div class="form-group">
        <label for="feedback" class="form-label">Tell us about your experience of the product or new features you would like to see:</label>
        <textarea id="feedback" v-model="feedback" class="form-control" placeholder="Enter your feedback here..." maxlength="1500" rows="8" />
        <p v-if="wordCount > 1500" class="word-count-warning">Please limit your feedback to 1500 words</p>
      </div>
      <div class="button-container">
        <button type="submit" class="btn send-button" :disabled="wordCount > 1500">{{ this.buttonText }}</button>
      </div>
      <p v-if="displayMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="displayError" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.form-group {
  width: 100%;
  max-width: 1200px; /* Increased max-width */
}

.form-label {
  display: block;
  font-weight: bold;
  margin-bottom: 10px;
}

.form-control {
  width: 100%;
  font-style: italic;
  font-size: 1rem;
  padding: .375rem .75rem;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2.5rem;
}

.send-button {
  border: 2px solid #0c952c;
  background-color: #ffffff;
  color: #0c952c;
  padding: .375rem 1.5rem; /* Increased padding to make button wider */
  max-width: 300px; /* Added max-width to limit button size */
}

.send-button:hover {
  background-color: #0c952c;
  color: #ffffff;
}

.word-count-warning,
.success-message,
.error-message {
  text-align: center;
}

.success-message {
  color: green;
}

.error-message {
  color: red;
}
</style>
