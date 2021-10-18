<template>
  <base-card>
    <form @submit.prevent="submitData">
      <div class="form-group">
        <div class="form-control">
          <span v-html=rectifiedQ(questionNo,question)></span>
        </div>
        <div v-for="(answer, ind) in answers" :key="ind" class="form-check">
          <input :id="id" :name="id" :value="ind" type="radio" class="form-check-input" v-model="yourAnswer" />
          <label v-html=answer class="form-check-label"></label>
        </div>
        <div>
          <button class="btn btn-success" type="submit" @click="updateAnswer">Save answer</button>
        </div>
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

  emits: {
    'update-answer': function(id, yourAnswer) {
      if (yourAnswer >= 0) {
        return true;
      } else {
        console.log("empty answer!!")
        return false;
      }
    }
  },

  watch: {
    id() {
      this.yourAnswer = this.givenAnswer
    }
  },
  methods: {
    updateAnswer() {
      
      if (this.yourAnswer !== this.givenAnswer){
        this.$emit('update-answer', this.id, this.yourAnswer);
      }
    },

    rectifiedQ(questionNo, question) {
      const Num = questionNo + 1
      const q = question.replace(/(<p[^>]+?>|<p>|<\/p>)/img, "");
      return '#' + Num.toString() + '. ' + q

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