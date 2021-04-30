<template>
    <div>
        <Navbar/>
        <v-row>
            <v-col lg="6">
                <div class="pa-3">
                <v-tabs v-model="tab">
                    <v-tab href='#tab-1'>Get Started</v-tab>
                    <v-tab href='#tab-2' :disabled="complete == 0">Pan Card</v-tab>
                    <v-tab href='#tab-3'>Login</v-tab>
                    <v-tab-item value='tab-1' class="mt-3 shadow-lg bg-light rounded-lg pa-4 blue-grey lighten-5 elevation-7">
                    
                            <v-file-input
                                accept="image/*"
                                label="Upload Aadhar (JPG/PNG)"
                                show-size
                                counter
                                v-model="aFile"
                                @change="getAadharInfo"
                            ></v-file-input>
                            <v-text-field
                            label="Name"
                            prepend-icon="mdi-account"
                            v-model="aName"
                            :rules="rules"
                            ></v-text-field>
                            <v-text-field
                            label="DOB"
                            prepend-icon="mdi-calendar"
                            v-model="aDob"
                            :rules="rules"
                            ></v-text-field>
                            <v-text-field
                            label="Gender"
                            prepend-icon="mdi-gender-male-female"
                            v-model="aGender"
                            :rules="rules"
                            ></v-text-field>
                            <v-text-field
                            label="Aadhar Number"
                            prepend-icon="mdi-fingerprint"
                            v-model="aadhar"
                            :rules="rules"
                            >
                            </v-text-field>
                            <div v-if="aExceptions.length>0">
                                <v-alert
                                border="left"
                                type="error"
                                >
                                    <span v-for="(ex,index) in aExceptions" :key="index">
                                        {{ex}}
                                    </span>
                                </v-alert>
                            </div>
                            <div class="text-right">
                                <v-btn color="primary" elevation="2" @click="complete=1;tab='tab-2'">Proceed<v-icon class="ml-2">mdi-arrow-right-bold </v-icon></v-btn>
                            </div>

                    </v-tab-item>
                    <v-tab-item value='tab-2' class="mt-3 shadow-lg bg-light rounded-lg pa-4 blue-grey lighten-5 elevation-7">
                        
                        <span>
                            <v-icon class="mr-2">mdi-newspaper-variant-multiple-outline</v-icon>
                            Select PAN Type</span>
                        <v-radio-group row v-model="panType">
                            <div class="row">
                                <div class="col-sm-6 text-center">
                                    <v-img src="../../assets/pan_format_1.jpg" contain width="50vh" class="mb-3"> </v-img>
                                    <v-radio :value="'old'" label="Old Layout"></v-radio>
                                </div>
                                <div class="col-sm-6 text-center">
                                    <v-img src="../../assets/pan_format_2.jpeg" contain width="50vh" class="mb-3"></v-img>
                                    <v-radio :value="'new'" label="New Layout"></v-radio>
                                </div>
                            </div>
                        </v-radio-group>
                        
                        <v-file-input
                                accept="image/*"
                                label="Upload Pan (JPG/PNG)"
                                show-size
                                counter
                                v-model="pFile"
                                @change="getPanInfo"
                            ></v-file-input>
                            <v-text-field
                            label="Name"
                            prepend-icon="mdi-account"
                            v-model="pName"
                            :rules="rules"
                            ></v-text-field>
                            <v-text-field
                            label="DOB"
                            prepend-icon="mdi-calendar"
                            v-model="pDob"
                            :rules="rules"
                            ></v-text-field>
                            <v-text-field
                            label="Father's Name"
                            prepend-icon="mdi-human-male-boy"
                            v-model="pFather"
                            :rules="rules"
                            ></v-text-field>
                            <v-text-field
                            label="PAN"
                            prepend-icon="mdi-card-account-details"
                            v-model="pan"
                            :rules="rules"
                            >
                            </v-text-field>
                            <div v-if="pExceptions.length>0">
                                <v-alert
                                border="left"
                                type="error"
                                >
                                    <span v-for="(ex,index) in pExceptions" :key="index">
                                        {{ex}}
                                    </span>
                                </v-alert>
                            </div>
                            <div class="text-right">
                                <v-btn color="primary" elevation="2" @click="dialog=true">Verify<v-icon class="ml-2">mdi-check-decagram </v-icon></v-btn>
                            </div>
                    </v-tab-item>
                    <v-tab-item value='tab-3' class="mt-3 shadow-lg bg-light rounded-lg pa-4 blue-grey lighten-5 elevation-7">
                        <div class="row">
                            <div class="col-8">
                                <v-text-field
                                    label="Phone Number"
                                    prepend-icon="mdi-phone"
                                    v-model="lPhone"
                                    :rules="phone_rule"
                                    :disabled="otpLoginSent"
                                ></v-text-field>
                            </div>
                            <div class="col-4 text-center">
                                <v-btn elevation="2" class="mt-4" @click="sendOTPLogin" :disabled="otpLoginSent">
                                    Send OTP
                                </v-btn>
                            </div>
                        </div>
                        <div class="row" v-if="otpLoginSent">
                            <div class="col-12">
                                <v-text-field
                                    label="OTP"
                                    prepend-icon="mdi-phone"
                                    v-model="lOtp"
                                ></v-text-field>
                            </div>
                        </div>
                        <div class="text-right" v-if="lOtp.length==6">
                                <v-btn color="primary" elevation="2" @click="verifyOTPLogin">Login<v-icon class="ml-2">mdi-login-variant</v-icon></v-btn>
                        </div>
                    </v-tab-item>
                </v-tabs>
                </div>
            </v-col>
            <v-col lg="6">
                <div class="pa-3">
                <h1 class="blue--text text--darken-3">About</h1>
                <hr>
                <div class="row">
                    <div class="col-lg-6">
                        <h2><br>
                            We strive to automate processes and enable users and organizations to:
                            <div>
                                <ul>
                                    <li>Open bank accounts easily</li>
                                    <li>Parse user info easily and store in databases.</li>
                                    <li>Reduce work and time required on both organization and user's end exponentially</li>
                                </ul>
                            </div>
                        </h2>
                    </div>
                    <div class="col-lg-6 pa-3">
                        <v-img src="../../assets/easyRpa.svg"></v-img>
                    </div>
                </div>
                </div>
            </v-col>
        </v-row>
        <v-dialog
        v-model="dialog"
          fullscreen
          hide-overlay
          transition="dialog-bottom-transition"
        >
        <v-card>
            <v-card-title class="headline  blue darken-3 white--text">
                Are You Sure?
            </v-card-title>
            <v-card-text class="pa-5">
                <span class="red--text text--lighten-1 text-h6">The following data will be used to verify and create your account. Please check before proceeding</span>
                <v-text-field
                label="Name"
                prepend-icon="mdi-account"
                v-model="pName"
                :rules="rules"
                ></v-text-field>
                <v-text-field
                label="DOB"
                prepend-icon="mdi-calendar"
                v-model="pDob"
                :rules="rules"
                ></v-text-field>
                <v-text-field
                label="Father's Name"
                prepend-icon="mdi-human-male-boy"
                v-model="pFather"
                :rules="rules"
                ></v-text-field>
                <v-text-field
                label="PAN"
                prepend-icon="mdi-card-account-details"
                v-model="pan"
                :rules="rules"
                ></v-text-field>
                
                <v-text-field
                label="Aadhar"
                prepend-icon="mdi-fingerprint"
                v-model="aadhar"
                :rules="rules"
                ></v-text-field>
                <div class="row">
                    <div class="col-10">
                        <v-text-field
                        :disabled="otpSent"
                        label="Phone Number"
                        prepend-icon="mdi-phone"
                        v-model="phone"
                        :rules="phone_rule"
                        ></v-text-field>
                    </div>
                    <div class="col-2 text-center">
                        <v-btn elevation="2" class="mt-4" @click="sendOTP" :disabled="otpSent">
                            Send OTP
                        </v-btn>
                    </div>

                </div>
                <div class="row" v-if="otpSent && verified">
                    <div class="col-10">
                        <v-text-field
                        label="OTP"
                        prepend-icon="mdi-phone"
                        v-model="otp"
                        
                        ></v-text-field>
                    </div>
                    <div class="col-2 text-center">
                        <v-btn elevation="2" class="mt-4" @click="verifyOTP">
                            Verify OTP
                        </v-btn>
                    </div>

                </div>
                <div class="text-right mt-4">
                    <v-btn color="primary" :disabled="verified" elevation="2" @click="signUp">Sign-Up<v-icon class="ml-2">mdi-login-variant </v-icon></v-btn>
                </div>
                </v-card-text>
        </v-card>
        </v-dialog>
    </div>
</template>
<script>
import axios from 'axios'
import Navbar from './Navbar'
import {createUserSession,getSessionUser} from '../../plugins/sessions'
export default {
    name:"Home",
    data() {
        return {
            tab:"tab-1",
            aName:"",
            aDob:"",
            aGender:"",
            aadhar:"",
            aExceptions:[],
            aFile:undefined,
            pName:"",
            pDob:"",
            pFather:"",
            pan:"",
            pExceptions:[],
            pFile:undefined,
            rules: [
            value => !!value || 'Required.'],
            complete:0,
            panType:"old",
            userInfo:{},
            dialog:false,
            phone:"",
            phone_rule:[
                value=>value.length<=10 || "Invalid Phone Number",
                value=>{return /^\d+$/.test(value) || "Numbers are only allowed"},
            ],
            otpSent:false,
            otp:"",
            verified:true,
            lOtp:"",
            lPhone:"",
            otpLoginSent:false,
        }
    },
    components:{
        Navbar
    },
    methods: {
        getAadharInfo(){
            if(this.aFile!=undefined){
                let formData = new FormData();
                formData.append('aadhar', this.aFile);
                let self = this
                const config={
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
                axios.post("http://127.0.0.1:8000/api/extract_aadhar_data",formData,config)
                .then((response)=>{
                    self.aName = response.data.name
                    self.aDob = response.data.dob
                    self.aGender = response.data.gender
                    self.aadhar = response.data.aadhar
                    self.aExceptions = response.data.exceptions
                    self.aFile=undefined
                })
            }
            
        },
        getPanInfo(){
             if(this.pFile!=undefined){
                let formData = new FormData();
                formData.append('pan', this.pFile);
                formData.append('type',this.panType)
                let self = this
                const config={
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
                axios.post("http://127.0.0.1:8000/api/extract_pan_data",formData,config)
                .then((response)=>{
                    self.pName = response.data.name
                    self.pDob = response.data.dob
                    self.pFather = response.data.father_name
                    self.pan = response.data.pan
                    self.pExceptions = response.data.exceptions
                    console.log(response.data)
                    self.pFile=undefined
                })
            }
        },
        sendOTP(){
            let payload={
                phone:this.phone
            }
            let self = this
            axios.post("http://127.0.0.1:8000/api/otp",payload)
            .then((response)=>{
                self.otpSent=true
                console.log(response.data)
            })
        },
        sendOTPLogin(){
            let payload={
                phone:this.lPhone
            }
            let self = this
            axios.post("http://127.0.0.1:8000/api/otp",payload)
            .then((response)=>{
                self.otpLoginSent=true
                console.log(response.data)
            })
        },
        verifyOTP(){
            let payload={
                phone:this.phone,
                otp:this.otp
            }
            let self = this
            axios.post("http://127.0.0.1:8000/api/otp_verification",payload)
            .then((response)=>{
                if(response.data.message=="Verified"){
                    self.verified=false
                    console.log(response.data)
                    alert('Phone Verified')
                }
                else{
                    alert('Wrong OTP')
                }
            })
        },
        verifyOTPLogin(){
            let payload={
                phone:this.lPhone,
                otp:this.lOtp
            }
            let self = this
            axios.post("http://127.0.0.1:8000/api/login",payload)
            .then((response)=>{
                if(response.data.message=="User Found"){
                    self.verified=false
                    console.log(response.data)
                    createUserSession(response.data['user'])
                    this.$router.push({ name: 'Dashboard' })
                }
                else{
                    console.log(response.data)
                    alert('Wrong OTP')
                }
            })
        },
        signUp(){
            let payload={
                name:this.pName,
                father:this.pFather,
                dob:this.pDob.split("/").reverse().join("-"),
                aadhar:this.aadhar,
                pan:this.pan,
                phone:this.phone,
            }
            axios.post("http://127.0.0.1:8000/api/signup",payload)
            .then((response)=>{
                alert(response.data.message)    
            })
        }
        
    },
    mounted() {
        if(getSessionUser()!=undefined){
            this.$router.push({ name: 'Dashboard' })
        }
    },
}
</script>