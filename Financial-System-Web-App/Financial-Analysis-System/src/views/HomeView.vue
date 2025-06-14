<script>
import { defineComponent } from 'vue';

// Components

import financialTable from '../components/financialTable.vue'
import financialGraph from '../components/financialGraph.vue'
import API_Handler from '../router/apiHandler.js'

export default defineComponent({
  name: 'HomeView',
  
  data() {
    return {
      API_Handler_Object: null,
      headers: [
          { title: 'Order Number', align: 'start', key: 'order_id' },
          { title: 'Type', align: 'end', key: 'order_type' },
          { title: 'Price (£)', align: 'end', key: 'price' },
          { title: 'Status', align: 'end', key: 'status' },
          { title: 'Table Number', align: 'end', key: 'table_number' },
        ],
      currentOrdersFiltered: null,
      imageURL: null,
    }
  },
  
  async mounted(){
    // Initialise API hanlding object if it's not created - code is present in all sections that use this object
    if (!this.API_Handler_Object){
      this.API_Handler_Object = new API_Handler()
    }

    // Place computed data into variables as binding async and computed variables is buggy in vue
    this.currentOrdersFiltered = await this.currentOrdersData
    this.imageURL = await this.imageDataURL
  },

  components: {
    financialTable,
    financialGraph
  },

  computed:{
    async imageDataURL(){      
      // Initialise API hanlding object if it's not created
      if (!this.API_Handler_Object){
        this.API_Handler_Object = new API_Handler()
      }

      // Get current date
      let currentDate = this.API_Handler_Object.formatDate(new Date()) // Convert from %d/%m/%Y to %Y-%m-%d
      console.log("Current Date:", currentDate);

      // Get date three months ago
      let pastDate = new Date();
      pastDate.setMonth(pastDate.getMonth() - 3);
      pastDate = this.API_Handler_Object.formatDate(pastDate) // Convert from %d/%m/%Y to %Y-%m-%d
      console.log("Date Three Months Ago:", pastDate);

      let orders = null
      try{
        // GET OrdersGraph query type - Returns blob object from receiving image for OrdersGraph query response 
        orders = await this.API_Handler_Object.getJSON_OrdersGraph(pastDate, currentDate, 1) // Pass user_id as 1 until Authention system integration
      }
      catch(ex) {
        console.log("Error getting graph: ", ex);
        return null
      }

      // Get URL from image blob
      return URL.createObjectURL(orders)
    },

    async currentOrdersData(){
      // Initialise API hanlding object if it's not created
      if (!this.API_Handler_Object){
        this.API_Handler_Object = new API_Handler()
      }

      // Get current date
      let currentDate = this.API_Handler_Object.formatDate(new Date()) // Convert from %d/%m/%Y to %Y-%m-%d
      console.log("Current Date:", currentDate);

      // Get date three months ago
      let pastDate = new Date();
      pastDate.setMonth(pastDate.getMonth() - 3);
      pastDate = this.API_Handler_Object.formatDate(pastDate) // Convert from %d/%m/%Y to %Y-%m-%d
      console.log("Date Three Months Ago:", pastDate);

      let orders = null
      try{
        // GET OrdersReport query type - Returns JSON object from receiving response from OrdersReport query - pass user id as 1 until authention system integration
        orders = this.API_Handler_Object.getJSON_Orders(pastDate, currentDate, 1)
      }
      catch(ex) {
        console.log("Error getting orders: ", ex);
        return null
      }

      return orders
    },
  },
});
</script>

<template>
  <main class="pt-5 mainContainer">
    <financialTable
      v-if="currentOrdersFiltered"
      :tableContainerPadding=8
      colour="grey"
      class="financialTable"
      :financialTableData=currentOrdersFiltered
      :financialTableHeaders=headers
      tableTitle="Last 3 months orders"
    />

    <financialGraph
      v-if="imageURL"
      :imageURL="imageURL"
      class="financialGraph"
      :graphContainerPadding=3
      graphTitle="Order revenue for last 3 months">
    </financialGraph>
  </main>
</template>


<style scoped>
.financialTable{
  padding-bottom: 3vh;
}

.financialGraph{
  padding-bottom: 3vh;
}

.mainContainer{
  display: flex;
  flex-direction: column;
  
  align-items: center;
  justify-content: center;
}
</style>