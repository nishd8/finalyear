<template>
    <v-card
    class="mx-auto my-12"
    max-width="600"
  >
    <v-img
      height="250"
      src="../../assets/6554.jpg"
    ></v-img>

    <v-card-title class="blue--text text--darken-3 justify-center">Recieve Money</v-card-title>
    
    <v-card-text>
        <v-img 
        height="300"
        width="300"
        class="mx-auto"
        :src="qr"></v-img>
    </v-card-text>


    <v-card-actions>
      <v-btn
        color="green darken-3"
        text
        class="ml-auto"
      >
        Send
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import axios from 'axios'
import {getSessionUser} from '../../plugins/sessions'
export default {
    name:"RecieveMoney",
    data() {
        return {
            qr:""
        }
    },
    methods: {
        getQr(){
            var payload={
                acc_id:getSessionUser()['acc_id']
            }
            var url = "http://127.0.0.1:8000/api/generate_qr"
            var self=this
            axios.post(url,payload).then((response)=>{
                self.qr="data:image/png;base64,"+response.data['qr_code']
                console.log(response.data)
            })
        }
    },
    mounted() {
        this.getQr()
    },
}
</script>