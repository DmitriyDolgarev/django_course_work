<script setup>
import useUserProfileStore from '@/stores/UserProfileStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const userProfileStore = useUserProfileStore()
const router = useRouter();

let login = ref();
let password = ref();

let user = ref({});

function onLoginClick() {
    userProfileStore.login(user);
    //router.push("/")
}
</script>

<template>

    <div class="back">
        <div class="inputBlock"> 
            <input
            type="text"
            class="form-control"
            v-model="user.username"
            required
            />
            <input
            type="password"
            class="form-control item"
            v-model="user.password"
            required
            />
            <button @click="onLoginClick" class="btn btn-primary item">
                Войти
            </button>
        </div>
    </div>
</template>

<style scoped>
.back{
  opacity: 1;
  transform: scale(1, 1);
  height: auto;

  display: flex;

  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  z-index: 1000;
  align-items: center;
  justify-content: center;

  background-image: url(https://a.d-cd.net/1d344bes-1920.jpg);
  background-position: center bottom;
  background-size: cover; /* Или background-size: contain; */
  background-repeat: no-repeat; /* Необязательно, но желательно */
}

.inputBlock{
    border-radius: 20px;
    background-color: rgba(255, 212, 84, 0.922);
    padding: 30px;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.item{
    margin-top: 10px;
}
</style>