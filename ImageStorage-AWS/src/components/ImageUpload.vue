<template>
<div v-loading="loading">
  <el-card class="box-card">
    <p>Upload images</p>
    <div>
      <el-upload
        :http-request="(params) => fileChange(params)"
        class="upload-demo"
        drag
        :before-upload="beforeAvatarUpload"
        action=""
        multiple>
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">drag to upload or <em>click upload</em></div>
        <template #tip>
          <div class="el-upload__tip">
            Only can upload jpg/png/jpeg
          </div>
        </template>
      </el-upload>
    </div>
  </el-card>
  <el-card class="search-box-card">
    <el-row>
        <el-col :span="12">
          <p>Search Image</p>
            <el-upload
              :http-request="findImg"
              class="avatar-uploader"
              action="https://jsonplaceholder.typicode.com/posts/"
              :show-file-list="false"
            >
              <img v-if="imageUrl" :src="imageUrl" class="avatar">
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
        </el-col>
        <el-col :span="12">
          <div>
              <el-select
                v-model="tagValue"
                multiple
                filterable
                allow-create
                default-first-option
                placeholder="please input tag">
              </el-select>
          </div>
          <div>
            <el-button type="primary" size="mini" @click="searchTag()">Search Tags</el-button>
          </div>
        </el-col>
    </el-row>
  </el-card>
  <el-card class="image-card">
    <template v-if="imgList.length">
      <div class="image-list-block" v-for="img, index in imgList" :key="index">
        <template v-if="img.url">
          <el-image
            style="width: 200px; height: 200px"
            :src="img.url"
            fit="fit"></el-image>
          <el-button class="delete-item" type="danger" icon="el-icon-delete" circle @click="deleteImg(img.url, index)"></el-button>
          <div class="tag">
            <el-tag
              :key="ind"
              v-for="tag, ind in img.tags"
              size="mini"
              :disable-transitions="false">
              {{tag}}
            </el-tag>
            <el-input
              class="input-new-tag"
              v-if="img.inputVisible"
              v-model="inputValue"
              :ref="`input${ind}`"
              size="mini"
              @keyup.enter="handleInputConfirm(img, ind)"
            >
            </el-input>
            <el-button v-else class="button-new-tag" size="mini" @click="showInput(img, ind)">+ New Tag</el-button>
          </div>
        </template>
      </div>
    </template>
    <template v-else>
      <div>
        <p>There are no pictures</p>
      </div>
    </template>
  </el-card>
</div>
</template>

<script>
import Auth from '@aws-amplify/auth';
import { AwsUpdate } from "@/utils/aws";
import { setToken } from "@/utils/auth";
export default {
    data() {
        return {
            imgList: [],
            inputValue: '',
            tagValue: [],
            imageUrl: '',
            imgUrl: "",
            loading: true
        }
    },
    mounted(){
        Auth.currentSession().then(res=>{
          let idToken = res.getIdToken()
          let jwt = idToken.getJwtToken()
          setToken(`Bearer ${jwt}`)
          Auth.currentCredentials().then(res => {
              console.log(res)
          })
          this.initImgList();
        })
    },
    
    methods:{
        initImgList() {
            HttpRequest.get('/test/images', {tags: "all"}).then(response => {
                this.imgList = response
            }).catch(error => {
                console.error(error);
            }).finally(() => {
                this.loading = false;
            })
        },

        beforeAvatarUpload(file) {
          const isJPG = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/jpg';
          if (!isJPG) {
            this.$message.error('the image must be jpeg, jpg, png');
          }
          return isJPG;
        },

        // upload
        fileChange(e) {
          this.loading = true;
          let file = e.file;
          AwsUpdate(file).then(res=>{
            setTimeout(() => {
              this.initImgList();
            }, 6000);
          })
        },

        findImg(e) {
          this.loading = true;
          let file = e.file;
          console.log(e,'e');
          let reader = new FileReader();
          if (file) {
              reader.readAsDataURL(file);
          }          
          reader.onload = () => {
              let base64Str = reader.result;
              let params = {
                file: base64Str
              }
              HttpRequest.post('/test/findimagebyimage', params).then(response => {
                this.loading = false;
                  if (response) {
                    this.imgList = response
                  } else {
                    this.imgList = []
                  }
              }).catch(error => {
                  console.error(error);
              }).finally(() => {
              })
          }
        },

        // add tag
        showInput(img, ind) {
          img.inputVisible = true;
          this.$nextTick(_ => {
            this.$refs[`input${ind}`].$refs.input.focus();
          });
        },

        handleInputConfirm(img) {
          let inputValue = this.inputValue;
          if (inputValue) {
            img.tags.push(inputValue);
          }
          img.inputVisible = false;
          this.inputValue = '';
          let params = {
            url: img.url,
            tags: img.tags.toString()
          }
          HttpRequest.post('/test/images', params).then(response => {
              console.log('response', response);
          }).catch(error => {
              console.error(error);
          }).finally(() => {

          })
        },

        searchTag() {
            this.loading = true;
            let params = {
              tags: this.tagValue.length > 0 ? this.tagValue.toString() : "all"
            }
            HttpRequest.get('/test/images', params).then(response => {
                this.loading = false;
                this.imgList = response
            }).catch(error => {
                console.error(error);
            }).finally(() => {

            })

        },
        deleteImg(url, index) {
            this.loading = true;
            // http
            HttpRequest.post('/test/delete', {url: url}).then(response => {
                this.loading = false;
                this.imgList.splice(index,1)
            }).catch(error => {
                console.error(error);
            }).finally(() => {

            })
        }
    }
}
</script>

<style scoped>
a {
  color: #42b983;
}
.image-card :deep().el-card__body {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.image-list-block {
  margin: 10px;
  position: relative;
}
.tag{
  max-width: 200px;
}
.tag span{
  margin: 0 2px 2px 2px;
}
.image-list-block .delete-item{
  position: absolute;
  right: 0;
  top: 0;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.search-box-card :deep().avatar-uploader .el-upload{
  border: 1px solid;
}
.search-box-card :deep().avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
