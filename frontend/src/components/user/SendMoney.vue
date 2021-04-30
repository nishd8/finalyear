<template>
    <v-card
    class="mx-auto my-12"
    max-width="600"
  >
    <v-img
      height="250"
      src="../../assets/6617.jpg"
    ></v-img>

    <v-card-title class="blue--text text--darken-3  justify-center">Send Money</v-card-title>
    <div v-if="!transactionComplete">
        <div v-if="!otpSent">
        <v-card-text>
            <div class="row">
                <div class="col-9">
                    <v-text-field
                        label="Reciever's Account Number"
                        prepend-icon="mdi-account-details"
                        v-model="r_acc_id"
                    ></v-text-field>
                </div>
                <div class="col-3">
                    <v-btn 
                    text
                    color="blue darken-3"
                    class="mt-5"
                    @click="dialog_open=true"
                    >
                        <v-icon class="mr-3">
                            mdi-qrcode-scan
                        </v-icon>
                        Scan QR
                    </v-btn>
                </div>
            </div>
            <v-text-field
                label="Amount"
                prepend-icon="mdi-cash-multiple"
                v-model="amount"
            ></v-text-field>
        </v-card-text>

        <v-card-actions class="mb-4">
          <v-btn
            color="green darken-3"
            text
            class="ml-auto"
            @click="sendMoneyOTP"
          >
            Verify
          </v-btn>
        </v-card-actions>
      
        </div>
        <div v-else>
          <v-card-text>
              <v-text-field
                  label="OTP"
                  prepend-icon="mdi-form-textbox-password"
                  v-model="otp"
              ></v-text-field>
          </v-card-text>

          <v-card-actions class="mb-4">
            <v-btn
              color="green darken-3"
              text
              class="ml-auto"
              @click="verifyOTPandSend"
            >
              Send
            </v-btn>
          </v-card-actions>
        </div>
    </div>
    <div v-else>
      <div class="pa-3">
        <v-img
        height="150"
        width="150"
        class="mx-auto"
        src="../../assets/transaction_success.gif"
      ></v-img>
      </div>
      <div class="green--text text--darken-3 text-center">
        <h3>Transaction Successful</h3>
      </div>
      <v-card-actions class="mt-3 mb-4">
            <v-btn
              color="green darken-3"
              text
              class="ml-auto"
              @click="transactionComplete=false"
            >
              Done
            </v-btn>
          </v-card-actions>
    </div>
    <ScannerDialog
      :dialog="dialog_open"
      @dialogClose="dialog_open=false"
      @qrDecode="decodeQR"
    />
  </v-card>
</template>
<script>
import { getSessionUser } from '../../plugins/sessions'
import ScannerDialog from './ScannerDialog'
import axios from 'axios'
export default {
    name:"SendMoney",
    components:{
      ScannerDialog
    },
    data() {
        return {
            r_acc_id:"",
            dialog_open:false,
            amount:null,
            otpSent:false,
            otp:null,
            transactionComplete:false
        }
    },
    methods: {
      decodeQR(val){
        this.r_acc_id=val;
        this.dialog_open=false
      },
      sendMoneyOTP(){
        let payload={
                phone:getSessionUser()['phone']
            }
            let self = this
            axios.post("http://127.0.0.1:8000/api/otp",payload)
            .then((response)=>{
                self.otpSent=true
                console.log(response.data)
            })
      },
      verifyOTPandSend(){
        var self=this
        let payload={
            sender:getSessionUser()['acc_id'],
            reciever:this.r_acc_id,
            otp:this.otp,
            amount:this.amount,
            phone:getSessionUser()['phone']
        }
        axios.post("http://127.0.0.1:8000/api/send_money",payload)
        .then((response)=>{
                self.r_acc_id=""
                self.otp=null
                self.amount=null
                self.otpSent=false
                self.transactionComplete=true
                console.log(response.data)
            })
        .catch((error)=>{
                self.r_acc_id=""
                self.otp=null
                self.amount=null
                self.otpSent=false
              alert(error.response.data['message'])          
        })
      }
    },
}
</script>