<template>
  <div class="container d-flex flex-column justify-content-center align-items-center text-center" style="min-height: 10vh;">
    <h1 class="display-4 mb-1 fw-bold">ReadSearch GPT</h1>  
    <h2 class="h3 mb-1 fw-bold" style="font-style: italic;">Get Results Without Searching</h2>
    <div class="card p-4 mb-4 mt-2 rounded shadow" style="max-width: 800px;">
      <div class="card-body">
        <p class="lead">Unlike ChatGPT using outdated information, ReadSearchGPT uses up-to-date internet information to answer your questions.</p>
        <p class="lead">ReadSearch frees you from spending hours sifting through online information and maintains your Privacy as we DO NOT track your personal information.</p>
      </div>
    </div>
    <div class="d-flex justify-content-center gap-5">
      <button @click="watchTutorial" class="btn btn-lg btn-info mr-3"> Tutorial Video </button> 
      <button @click="goToNextPage" class="btn btn-lg btn-success">Get Started</button>
    </div>
    <div v-if="showModal" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <span class="close" @click.stop="closeModal">&times;</span>
        <div class="video-wrapper">
            <iframe :src="'https://www.youtube.com/embed/pkS46QVw664'" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          </div>      
      </div>
    </div>
  </div>
</template>

  
  <script>
  export default {
    data() {
    return {
      showModal: false,
    };
  },
    methods: {
      goToNextPage() {
        this.$router.push({ path: '/newsearch' });
      },
      watchTutorial() {
      this.showModal = true;
    },
      closeModal() {
      this.showModal = false;
    },
    },
  };
  </script>
  
  <style scoped>
h3, .lead {
  color: #333;
}
.btn-success {
  background-color: #0c952c;
  border-color: #0c952c;
}
.btn-success:hover {
  background-color: #006c22;
  border-color: #006c22;
}
.btn-info {
  background-color: #17a2b8;
  border-color: #17a2b8;
}
.btn-info:hover {
  background-color: #138496;
  border-color: #138496;
}
h1, h2 {
  color: #5781c0;
}
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}
.modal-content {
  position: relative;
  background-color: #fefefe;
  border: 1px solid #888;
  width: 50%; /* Adjust as needed, percentage for responsiveness */
  height: 60%; /* Adjust as needed, viewport units for responsiveness */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px 10px;
}
.close {
  position: absolute;
  top: 5px; /* Adjust as per requirement */
  right: 15px; /* Adjust as per requirement */
  color: #aaaaaa;
  font-size: 28px;
  font-weight: bold;
}
.close:hover, .close:focus {
  color: #0e0e0e;
  text-decoration: none;
  cursor: pointer
}
.video-wrapper {
  position: relative;
  overflow: hidden;
  padding-top: 56.25%; /* for 16:9 aspect ratio */
  width: 100%;
  height: 0;
}

.video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
@media (max-width: 768px) {
  .modal-content {
    width: 560px; /* Preferred width for larger screens */
    height: 315px; /* Preferred height for larger screens */
  }
  .video-wrapper {
    padding-top: 50%; /* reset to default aspect ratio */
  }
}
</style>
