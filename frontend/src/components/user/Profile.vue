<template>
  <v-card
    class="mx-auto my-12 "
    max-width="600"
  >
    
    <br>
    <v-img
        height="200"
        width="200"
        src="../../assets/account-circle.svg"
        class="mx-auto"
    ></v-img>
    <br>
    <v-card-title>{{user.name}}</v-card-title>
    <v-divider class="mx-4"></v-divider>

    <v-card-text>
      <div class="mb-3">
            Account Number
            <h3>{{user.acc_id}}</h3>
      </div>
      <div class="mb-3">
            Father
            <h3>{{user.father}}</h3>
      </div>
       <div class="mb-3">
            Aadhar Number
            <h3>{{user.aadhar}}</h3>
      </div>
      <div class="mb-3">
            PAN
            <h3>{{user.pan}}</h3>
      </div>
      <div class="mb-3">
            Phone
            <h3>{{user.phone}}</h3>
      </div>
    </v-card-text>
    <v-card-text>
        <v-row
        align="center"
        class="mx-0"
        >
        <div class="grey--text">
          Profile Completion -
          <span v-if="user.status==false" class="ml-2 red--text">Verification Pending</span>
          <span v-else class="ml-2 green--text">Verified</span>
        </div>
        <v-progress-linear
            v-model="progress"
            class="mt-2"
        ></v-progress-linear>
      </v-row>
    </v-card-text>
    <div class="pa-2 text-right">
      <v-btn
        color="red darken-1"
        text
        @click="logout($router)"
      >
       Logout <v-icon class="ml-2">mdi-logout-variant</v-icon> 
      </v-btn>
    </div>
  </v-card>
</template>
<script>
import {logout} from '../../plugins/sessions'
  export default {
    name:"Profile",
    props:{
        user:Object
    },
    data() {
        return {
            progress:0
        }
    },
    methods: {
        logout
    },
    mounted() {
        if(this.user.status){
            this.progress=100
        }
        else{
            this.progress=90
        }
    },
  }
</script>