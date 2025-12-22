<template>
  <div>
    <div class="naslov">
      <h1>Nogometna Aplikacija</h1>
    </div>

    <div class="podnaslovne_stvari">
      <h2 style="text-align: center;">Kreirajte vlastitu ligu i timove </h2>
      <h2 style="text-align: center;">Najvažnije, zabavite se!</h2>
    </div>  
  </div>
</template>

<script>
  import {Auth} from '@/components/registracija'

  export default {
    data: () => ({
      ...Auth.state
    }),
  }
</script>

<style>
  body
    {
    background-image: linear-gradient(rgba(0, 0, 0, 0.20), rgba(0, 0, 0, 0.20)), url(https://studentski.hr/system/pictures/images/5/original/3a55c38d6c18374ba244590a2117d169dc09d0d7.jpg?1440585212); 
    background-size: cover; 
    z-index: -1;
    color: white;
  }

  .naslov
  {
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    text-align: center;
    color: white;
    margin-top:120px;
  }
  
  h1
  {
    font-size: 150px;
  }

  .podnaslovne_stvari 
  {
    margin-top: 10%;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    color: white;
  }

  h2
  {
    font-size: 80px;
  }
</style>