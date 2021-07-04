<template>
  <amplify-authenticator username-alias="email">
    <div v-if="authState !== 'signedin'">You are signed out.</div>
    <amplify-sign-up
      header-text="Sign Up Now!"
      slot="sign-up"
      :formFields="formFields"
    ></amplify-sign-up>
    <div v-if="authState === 'signedin' && user">
      <image-upload></image-upload>
    </div>
    <amplify-sign-out></amplify-sign-out>
  </amplify-authenticator>
</template>

<script>
import ImageUpload from './ImageUpload.vue'
import { onAuthUIStateChange } from '@aws-amplify/ui-components'
export default {
  components: { ImageUpload },
  name: 'HelloWorld',
  created() {
    this.unsubscribeAuth = onAuthUIStateChange((authState, authData) => {
      this.authState = authState;
      this.user = authData;
    })
  },
  mounted() {
    setTimeout(() => {
      this.formFields = [
            {
              type: "username",
              label: "Email *",
              placeholder: "Email",
              required: true,
            },
            {
              type: "password",
              required: true,
            },
            {
              type: "given_name",
              label: "First Name *",
              placeholder: "First Name",
              required: true,
            },
            {
              type: "family_name",
              label: "Last Name *",
              placeholder: "Last Name",
              required: true,
            },
          ]
          
    }, 1);
  },
  data() {
    return {
      user: undefined,
      authState: undefined,
      unsubscribeAuth: undefined,
      formFields: []
    }
  },
  beforeUnmount() {
    this.unsubscribeAuth();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
