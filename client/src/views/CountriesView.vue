<script setup>

import {computed, ref, onBeforeMount} from 'vue';
import axios from "axios";
import Cookies from 'js-cookie';

onBeforeMount(() => {
  axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
})

const countries = ref([]);
const countryToAdd = ref([]);
const countryToEdit = ref([]);

let countriesCount = ref();
let mostPopularCountry = ref();

async function fetchCountries()
{
  const r_countries = await axios.get("/api/countries/");
  const r_stats = await axios.get("/api/cars/stats/");
  const r_countries_stats = await axios.get("/api/countries/stats/");

  let stats = r_stats.data;
  mostPopularCountry = stats.most_country;

  let countries_stats = r_countries_stats.data;
  countriesCount = countries_stats.count;


  countries.value = r_countries.data;

  console.log(countries.value);
}

onBeforeMount(async () => {
  await fetchCountries();
})

async function onCountryAdd() {
  console.log(countryToAdd.value);
  await axios.post("/api/countries/", {
    ...countryToAdd.value,
  });
  
  await fetchCountries(); // переподтягиваю
}

async function onCountryEditClick(country)
{
  countryToEdit.value = { ...country };
}

async function onUpdateCountry()
{
  console.log(countryToEdit.value);
  await axios.put(`/api/countries/${countryToEdit.value.id}/`, {
    ...countryToEdit.value,
  });
  await fetchCountries();
}

async function onRemoveClick(country) {
  await axios.delete(`/api/countries/${country.id}/`);
  await fetchCountries(); // переподтягиваю
}

</script>

<template>

<form @submit.prevent.stop="onCountryAdd">
    <div class="row">
        <div class="col">
        <div class="form-floating">
            <input
            type="text"
            class="form-control"
            v-model="countryToAdd.name"
            required
            />
            <label for="floatingInput">Страна</label>
        </div>
        </div>
        <div class="col-1">
        <button class="btn btn-primary">
            Добавить
        </button>
        </div>
    </div>
</form>

<div class="modal fade" id="editMarkModal" role="dialog" tabindex="-1" aria-hidden="true">
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
                        v-model="countryToEdit.name"
                    />
                    <label for="floatingInput">Марка</label>
                    </div>
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
                @click="onUpdateCountry"
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
      <div class="statsHeader">{{ countriesCount }}</div>
      <h6>Количество стран</h6>
    </div>
    <div class="statsItem second">
      <div class="statsHeader">{{ mostPopularCountry }}</div>
      <h6>Самая популярная страна</h6>
    </div>
  </div>
</div>

<div v-for="item in countries" class="item">
    {{ item.name }}
    <button class="btn btn-danger" @click="onRemoveClick(item)">
      <i class="bi bi-x"></i>
    </button>
    <button
    type="button"
    class="btn btn-success"
    @click="onCountryEditClick(item)"
    data-bs-toggle="modal"
    data-bs-target="#editMarkModal"
    >
    <i class="bi bi-pen-fill"></i>
    </button>
</div>

</template>

<style scoped>

.item{
  margin: 15px;
  padding: 5px 20px;
  box-shadow: 10px 5px 5px rgba(128, 128, 128, 0.689);
  border-radius: 15px;

  display: grid;
  grid-template-columns: 17fr 1fr 1fr;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
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

</style>