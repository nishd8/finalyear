<template>
    <v-row class="justify-center">
        <v-dialog
            v-model="dialog"
            persistent
            max-width="400"
        >
            <v-card>
                <v-card-title class="headline">
                Scan QR
                </v-card-title>
                <v-card-text class="text-center">
                    <video autoplay="true" id="videoElement"
                        height="300"
                        width="300"
                    ></video>
                </v-card-text>
                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="green darken-1"
                    text
                    @click="closeDialog"
                >
                    Cancel
                </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
</template>
<script>
import QrcodeDecoder from 'qrcode-decoder';
export default {
    name:"ScannerDialog",
    props:{
        dialog:Boolean
    },
    methods: {
        closeDialog(){
            var video = document.getElementById("videoElement");
            console.log(video)
            this.stop(video)
            this.$emit('dialogClose');
        },
        stop(video) {
            var stream = video.srcObject;
            var tracks = stream.getTracks();

            for (var i = 0; i < tracks.length; i++) {
                var track = tracks[i];
                console.log(track)
                track.stop();
            }

            video.srcObject = null;
        },
        requestCamera(){
            var self=this
            if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (stream) {
                var video = document.getElementById("videoElement");
                video.srcObject = stream;
                var qr = new QrcodeDecoder();
                
                qr.decodeFromCamera(video).then((res) => {
                     self.stop(video)
                     self.$emit('qrDecode',res.data);
                });
                })
                .catch(function (error) {
                console.log("Something went wrong!" + error);
                });
            }
        }
    },
    watch:{
        dialog:function(){
            if(this.dialog==true){
                this.requestCamera()
            }
        }
    }
}
</script>