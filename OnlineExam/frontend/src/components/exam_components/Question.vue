<template>
  <base-card>
    <form @submit.prevent="submitData">
      <div class="form-control">
        <b>{{ questionNo + 1}}.</b><p v-html=question></p>
      </div>
      <div v-for="(answer, ind) in answers" :key="ind" class="form-control">
        <input :id="id" :name="id" :value="ind" type="radio" v-model="yourAnswer" />
        <label v-html=answer></label>
      </div>
      <div>
        <base-button type="submit">Save answer</base-button>
      </div>
    </form>
  </base-card>
</template>

<script>
export default {
  data() {
    return {
      inputIsInvalid: false,
      yourAnswer: this.givenAnswer
    };
  },
  props:['id', 'questionRefCode', 'questionNo', 'question', 'answers', 'givenAnswer' ],

  watch: {
    id() {
      this.yourAnswer = this.givenAnswer
    }
  },
  methods: {
    submitData() {
      if (this.yourAnswer !== this.givenAnswer){
        this.$emit('submit-data', this.id, this.yourAnswer);
        console.log("1111111111111111")
      }
      console.log(this.yourAnswer)
    }

  },
};
</script>

<style scoped>
label {
  font-weight: bold;
  margin-bottom: 0.5rem;
}

input {
  display: inline-block;
  font: inherit;
  padding: 0.15rem;
  border: 1px solid #ccc;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #3a0061;
  background-color: #f7ebff;
}

.form-control {
  margin: 1rem 0;
}
</style>