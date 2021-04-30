<template>
    <v-card
    class="mx-auto my-12"
    max-width="600"
  >
    <v-img
      height="250"
      src="../../assets/transaction.jpg"
    ></v-img>

    <v-card-title class="blue--text text--darken-3 justify-center">Transactions</v-card-title>
    
    <v-card-text style="height:350px;overflow-y:auto">
        <div v-for="(transaction,index) in transactions" :key="index" class="indigo lighten-5 rounded pa-3 mb-3">
            <div class="row">
                <div class="col-2 text-center">
                    <div class="blue darken-3 rounded-circle white--text text-center pa-4" style="height:50px;width:50px;font-size:25px;">
                        <span>
                            {{transaction.second_party[0]}}
                        </span>
                    </div>
                </div>
                <div class="col-7">
                    <div class="pa-1">
                        <h2>{{transaction.second_party}}</h2>
                        {{transaction.time_stamp_formatted}}
                    </div>
                </div>
                <div class="col-3 text-center">
                    <div class="pa-3">
                        <div v-if="transaction.sender_id==user" class="red--text text--darken-3">
                            <v-icon class="red--text text--darken-3">
                                mdi-arrow-top-right-thick
                            </v-icon>
                            {{transaction.amount}}
                        </div>
                        <div v-else class="green--text text--darken-3">
                            <v-icon class="green--text text--darken-3">
                                mdi-arrow-bottom-right-thick
                            </v-icon>
                            {{transaction.amount}}
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </v-card-text>


    <v-card-actions>
      <v-btn
        color="green darken-3"
        text
        class="ml-auto"
        @click="doc_gen"
      >
        Download
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import axios from 'axios'
import { getSessionUser } from '../../plugins/sessions'
import jsPDF from 'jspdf'
import 'jspdf-autotable'
export default {
    name:"Transactions",
    data() {
        return {
            transactions:[],
            user:getSessionUser()['acc_id']
        }
    },
    methods: {
        get_transaction(){
            var url = "http://127.0.0.1:8000/api/get_transaction?acc_id="+getSessionUser()['acc_id']
            
            var self=this
            axios.get(url).then((response)=>{
                self.transactions=response.data
                console.log(response.data)
            })
        },
        doc_gen(){
            console.log('sasas')
            var doc = new jsPDF()
            var date= new Date()
            // From Javascript
            var finalY = doc.lastAutoTable.finalY || 10
            doc.text('Bank Statement', 85, finalY + 15)
            doc.text(date.toDateString(), 85, finalY + 25)
            var table={
                startY: finalY + 35,
                head: [['ID', 'Name', 'Account','Debit', 'Credit','Time','Date']],
                body: [],
            }
            for(var i =0;i<this.transactions.length;i++){
                var temp=[]
                temp.push((i+1).toString())
                temp.push(this.transactions[i]['second_party'])
                
                if(this.transactions[i]['sender_id']==this.user){
                    temp.push(this.transactions[i]['reciever_id'])
                    temp.push(this.transactions[i]['amount'])
                    temp.push('')                    
                }
                else{
                    temp.push(this.transactions[i]['sender_id'])
                    temp.push('')
                    temp.push(this.transactions[i]['amount'])
                }
                temp.push(this.transactions[i]['time_stamp_formatted'].split(' ')[1])
                temp.push(this.transactions[i]['time_stamp_formatted'].split(' ')[0])
                table.body.push(temp)
            }
            doc.autoTable(table)
            doc.save(this.user+'.pdf')


        }
        
    },
    mounted() {
        this.get_transaction()
    },
}
</script>