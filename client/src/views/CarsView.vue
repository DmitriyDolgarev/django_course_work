<script setup>
import {computed, ref, onBeforeMount, watch} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';
import { storeToRefs } from 'pinia';
import useUserProfileStore from '@/stores/UserProfileStore';

const userProfileStore = useUserProfileStore();
const {
  is_auth, 
  username, 
  is_superuser
} = storeToRefs(userProfileStore);


onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const cars = ref([]);
const marks = ref([]);
const car_classes = ref([]);
const body_types = ref([]);
const countries = ref([]);

let carsList = ref([]);

let marksFilt = ref([]);
let car_classesFilt = ref([]);
let body_typesFilt = ref([]);
let countriesFilt = ref([]);

const carToAdd = ref({});
const carToEdit = ref({});
const carsPictureRef = ref();
const carsPictureRefForEdit = ref();
const carAddImageUrl = ref();
const carEditImageUrl = ref();

let isEnlargedImg = ref(false);
let currentImgSrc = ref("");
let box = ref();
let img = ref();

let usersToFilter = ref([]);
const allUsers = "Все";

let userToFilt = ref();

let carsCount = ref();
let mostPopularMark = ref();
let mostPopularBodyType = ref();

let markToFilter = ref();
let classToFilter = ref();
let bodyTypeToFilter = ref();
let countryToFilter = ref();

watch(markToFilter, () => {
  filterCars();
});
watch(classToFilter, () => {
  filterCars();
});
watch(bodyTypeToFilter, () => {
  filterCars();
});
watch(countryToFilter, () => {
  filterCars();
});
watch(userToFilt, () => {
  filterCars();
})

function filterCars()
{
  carsList = cars.value;
  
  if (userToFilt.value != allUsers && userToFilt.value != null)
  {
    carsList = carsList.filter(item => item.username == userToFilt.value);
  }
  if (markToFilter.value != allUsers && markToFilter.value != null)
  {
    carsList = carsList.filter(item => item.mark_name.name == markToFilter.value);
  }
  if (classToFilter.value != allUsers && classToFilter.value != null)
  {
    carsList = carsList.filter(item => item.car_class.name == classToFilter.value);
  }
  if (bodyTypeToFilter.value != allUsers && bodyTypeToFilter.value != null)
  {
    carsList = carsList.filter(item => item.body_type.name == bodyTypeToFilter.value);
  }
  if (countryToFilter.value != allUsers && countryToFilter.value != null)
  {
    carsList = carsList.filter(item => item.country.name == countryToFilter.value);
  }

  console.log("carsList");
  console.log(carsList);
  //carsList.value = arr.value;
}

async function fetchCars()
{
  const r = await axios.get("/api/cars/");
  const r_marks = await axios.get("/api/marks/");
  const r_classes = await axios.get("/api/car-classes/");
  const r_body_types = await axios.get("/api/body-types/");
  const r_countries = await axios.get("/api/countries/");

  const r_stats = await axios.get("/api/cars/stats/");

  cars.value = r.data;
  carsList.value = r.data;

  marks.value = r_marks.data;
  car_classes.value = r_classes.data;
  body_types.value = r_body_types.data;
  countries.value = r_countries.data;

  marksFilt = r_marks.data.map(item => item.name);
  car_classesFilt = r_classes.data.map(item => item.name);
  body_typesFilt = r_body_types.data.map(item => item.name);
  countriesFilt = r_countries.data.map(item => item.name);

  marksFilt.unshift(allUsers);
  car_classesFilt.unshift(allUsers);
  body_typesFilt.unshift(allUsers);
  countriesFilt.unshift(allUsers);

  //markToFilter = marksFilt[0];
  //classToFilter = car_classesFilt[0];
  //bodyTypeToFilter = body_typesFilt[0];
  //countryToFilter = countriesFilt[0];

  let stats = r_stats.data;
  carsCount = stats.count;
  mostPopularMark = stats.most_mark_name;
  mostPopularBodyType = stats.most_body_type;


  let users = cars.value.map(car => car.username);
  users = users.filter(user => user != null);
  usersToFilter = Array.from(new Set(users));
  usersToFilter.unshift(allUsers); 

  //userToFilt = usersToFilter[0];

  console.log(usersToFilter);
}

async function onLoadClick()
{
  await fetchCars();
}

onBeforeMount(async () => {
  await fetchCars();

  if (!is_superuser.value)
  {
    userToFilt = allUsers;
  }
  console.log(username);
})

async function onCarAdd() {
  const formData = new FormData();

  formData.append('picture', carsPictureRef.value.files[0]);
  formData.set('model', carToAdd.value.model);
  formData.set('mark_name', carToAdd.value.mark_name);
  formData.set('car_class', carToAdd.value.car_class);
  formData.set('body_type', carToAdd.value.body_type);
  formData.set('country', carToAdd.value.country);

  console.log(formData.value);
  await axios.post("/api/cars/", formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  
  await fetchCars(); // переподтягиваю
}

async function onRemoveClick(car) {
  await axios.delete(`/api/cars/${car.id}/`);
  await fetchCars(); // переподтягиваю
}

async function onCarEditClick(car)
{
  carToEdit.value = { ...car };
  carEditImageUrl.value = car.picture;
}

async function onUpdateCar()
{
  const formDataToEdit = new FormData();

  formDataToEdit.append('picture', carsPictureRefForEdit.value.files[0]);
  formDataToEdit.set('model', carToEdit.value.model);
  formDataToEdit.set('mark_name', carToEdit.value.mark_name);
  formDataToEdit.set('car_class', carToEdit.value.car_class);
  formDataToEdit.set('body_type', carToEdit.value.body_type);
  formDataToEdit.set('country', carToEdit.value.country);

  console.log(formDataToEdit.value);
  await axios.put(`/api/cars/${carToEdit.value.id}/`, formDataToEdit, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  /*
  console.log(carToEdit.value);
  await axios.put(`/api/cars/${carToEdit.value.id}/`, {
    ...carToEdit.value,
  });
  */

  await fetchCars();
}

async function carsAddPictureChange()
{
  carAddImageUrl.value = URL.createObjectURL(carsPictureRef.value.files[0]);
}
async function carsEditPictureChange()
{
  carEditImageUrl.value = URL.createObjectURL(carsPictureRefForEdit.value.files[0]);
}

function onImgClick(item)
{
  isEnlargedImg.value = true;
  currentImgSrc.value = item.picture;
}

function onZoomBoxClick()
{
    isEnlargedImg.value = false;
}

const exportData = async (format) => {
  const url = `/api/cars/export-${format}/`;
  try {
    const response = await axios.get(url, { responseType: "blob" });
    const blob = new Blob([response.data]);
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `cars.${format === "excel" ? "xlsx" : "docx"}`;
    link.click();
    URL.revokeObjectURL(link.href);
  } catch (error) {
    console.error("Ошибка при экспорте данных:", error);
  }
};

</script>

<template>
  <Transition>
  <div v-if="isEnlargedImg" id="zoomBox" class="zoomedBox" @click="onZoomBoxClick">
    <img id="zoomedImg" :src="currentImgSrc" class="enlarged" alt="">
  </div>
</Transition>

  <!-- ТУТ ПОДКЛЮЧИЛ обработчик отправки формы -->
  <form @submit.prevent.stop="onCarAdd">
    <div class="row">
      <div class="col">
        <div class="form-floating">
          <!-- ТУТ ПОДКЛЮЧИЛ studentToAdd.name -->
          <input
            type="text"
            class="form-control"
            v-model="carToAdd.model"
            required
          />
          <label for="floatingInput">Модель</label>
        </div>
      </div>
      <div class="col-1">
          <!-- А ТУТ ПОДКЛЮЧИЛ К select -->
        <div class="form-floating">
          <select class="form-select" v-model="carToAdd.mark_name" required>
            <option v-for="mark in marks" :value="mark.id">{{ mark.name }}</option>          </select>
          <label for="floatingInput">Марка</label>
        </div>
      </div>
      <div class="col-1">
        <div class="form-floating">
          <select class="form-select" v-model="carToAdd.car_class" required>
            <option :value="cls.id" v-for="cls in car_classes">{{ cls.name }}</option>
          </select>
          <label for="floatingInput">Класс</label>
        </div>
      </div>
      <div class="col-1">
        <div class="form-floating">
          <select class="form-select" v-model="carToAdd.body_type" required>
            <option :value="types.id" v-for="types in body_types">{{ types.name }}</option>
          </select>
          <label for="floatingInput">Кузов</label>
        </div>
      </div>
      <div class="col-1">
        <div class="form-floating">
          <select class="form-select" v-model="carToAdd.country" required>
            <option :value="country.id" v-for="country in countries">{{ country.name }}</option>
          </select>
          <label for="floatingInput">Страна</label>
        </div>
      </div>
      <div class="col-auto">
        <input class="form-control" type="file" ref="carsPictureRef" @change="carsAddPictureChange">
      </div>
      <div class="col-auto">
        <img :src="carAddImageUrl" style="max-height: 60px" alt="">
      </div>
      <div class="col-1">
        <button class="btn btn-primary">
          Добавить
        </button>
      </div>
    </div>
  </form>

  <div>
    
    <div class="modal fade" id="editCarModal" role="dialog" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Редактировать
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="carToEdit.model"
                  />
                  <label for="floatingInput">Модель</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="carToEdit.mark_name">
                    <option :value="mark.id" v-for="mark in marks">
                      {{ mark.name }}
                    </option>
                  </select>
                  <label for="floatingInput">Марка</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="carToEdit.car_class">
                    <option :value="cls.id" v-for="cls in car_classes">{{ cls.name }}</option>
                  </select>
                  <label for="floatingInput">Класс</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="carToEdit.body_type">
                    <option :value="types.id" v-for="types in body_types">{{ types.name }}</option>
                  </select>
                  <label for="floatingInput">Кузов</label>
                </div>
              </div>
              <div class="col-auto">
                <div class="form-floating">
                  <select class="form-select" v-model="carToEdit.country">
                    <option :value="country.id" v-for="country in countries">{{ country.name }}</option>
                  </select>
                  <label for="floatingInput">Страна</label>
                </div>
              </div>
              <div class="col-auto">
                <input class="form-control" type="file" ref="carsPictureRefForEdit" @change="carsEditPictureChange">
              </div>
              <div class="col-auto">
                <img :src="carEditImageUrl" style="max-height: 60px" alt="">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              data-bs-dismiss="modal"
              type="button"
              class="btn btn-primary"
              @click="onUpdateCar"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="stats">
      <h3>Статистика</h3>
      <div class="statsRow">
        <div class="statsItem first">
          <div class="statsHeader">{{ carsCount }}</div>
          <h6>Количество автомобилей</h6>
        </div>
        <div class="statsItem second">
          <div class="statsHeader">{{ mostPopularMark }}</div>
          <h6>Самая популярная марка</h6>
        </div>
        <div class="statsItem third">
          <div class="statsHeader">{{ mostPopularBodyType }}</div>
          <h6>Самый популярный тип кузова</h6>
        </div>
      </div>
    </div>

    <div v-if="is_superuser">
      <h3 class="filterHeader">Фильтрация по пользователю</h3>
      <div class="col-2 selectUser">
        <div class="form-floating">
          <select class="form-select" v-model="userToFilt">
            <option :value="user" v-for="user in usersToFilter">{{ user }}</option>
          </select>
          <label for="floatingInput">Пользователь</label>
        </div>
      </div>
    </div>

    <h3 class="filterHeader">Фильтрация</h3>
    <div class="row">
      <div class="col-2">
        <div class="form-floating">
          <select class="form-select" v-model="markToFilter" required>
            <option v-for="mark in marksFilt" :value="mark">{{ mark }}</option>
          </select>
          <label for="floatingInput">Марка</label>
        </div>
      </div>
      <div class="col-3">
        <div class="form-floating">
          <select class="form-select" v-model="classToFilter" required>
            <option :value="cls" v-for="cls in car_classesFilt">{{ cls }}</option>
          </select>
          <label for="floatingInput">Класс</label>
        </div>
      </div>
      <div class="col-2">
        <div class="form-floating">
          <select class="form-select" v-model="bodyTypeToFilter" required>
            <option :value="types" v-for="types in body_typesFilt">{{ types }}</option>
          </select>
          <label for="floatingInput">Кузов</label>
        </div>
      </div>
      <div class="col-2">
        <div class="form-floating">
          <select class="form-select" v-model="countryToFilter" required>
            <option :value="country" v-for="country in countriesFilt">{{ country }}</option>
          </select>
          <label for="floatingInput">Страна</label>
        </div>
      </div>
    </div>

    <div class="buttonsRow">
      <button 
        type="button"
        class="btn btn-success excelBtn"
        @click="exportData('excel')">
        <i class="bi bi-file-earmark-spreadsheet"></i>
      </button>
      <button 
        type="button"
        class="btn btn-primary excelBtn"
        @click="exportData('word')">
        <i class="bi bi-file-word"></i>
      </button>
    </div>

    <div v-for="item in carsList" class="carItem">

      {{ item.mark_name.name }} {{ item.model }}
      <div v-show="item.picture" @click="onImgClick(item)"><img :src="item.picture" class="usualImg" alt=""></div>
      <button
      type="button"
      class="btn btn-success"
      @click="onCarEditClick(item)"
      data-bs-toggle="modal"
      data-bs-target="#editCarModal"
      >
        <i class="bi bi-pen-fill"></i>
      </button>
      <button class="btn btn-danger" @click="onRemoveClick(item)">
        <i class="bi bi-x"></i>
      </button>

    </div>

  </div>

</template>

<style scoped>

.buttonsRow{
  width: 100px;
  margin: 30px;
  display: flex;
  flex-direction: row;

  justify-content: space-between;
}

.btn{
  width: auto;
}

.selectUser{
  margin-top: 15px;
}

.itemImgBox{
  border-radius: 15px;
  cursor: pointer;
}

.carItem{
  margin: 15px;
  padding: 5px 20px;
  box-shadow: 10px 5px 5px rgba(128, 128, 128, 0.689);
  border-radius: 15px;

  display: grid;
  grid-template-columns: 14fr 4fr 1fr 1fr;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}
.excelBtn{
  width: 40px;
  height: 40px;
}
.zoomedBox{
  opacity: 1;
  transform: scale(1, 1);
  height: auto;

  overflow: hidden;
  display: flex;

  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  backdrop-filter: blur(3px);
  z-index: 1000;
  align-items: center;
  justify-content: center;

}
.usualImg{
  max-height: 90px;
  border-radius: 15px;
  cursor: pointer;
}
.large{
  height: 250px;
}
.enlarged {
  max-width: 100%;
  z-index: 1000; /* Устанавливаем высокий z-index, чтобы изображение было поверх других элементов */
}

.enlarged img {
  max-width: 100%; /* Масштабируем изображение, чтобы оно занимало всю доступную ширину */
  max-height: 100%; /* Масштабируем изображение, чтобы оно занимало всю доступную высоту */
}

.stats{
  margin: 30px;
}
.statsRow{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
}
.statsItem{
  margin: 20px;
  padding: 40px;
  border-radius: 15px;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.first{
  background-color: #FFF685;
}
.second{
  background-color: #FFABD6;
}
.third{
  background-color: #A0D2EB;
}
.statsHeader{
  font-size: 40px;
  font-weight: bold;
}

.filterHeader{
  margin: 30px;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>