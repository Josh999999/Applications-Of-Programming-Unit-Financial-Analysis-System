<script>
import { defineComponent } from 'vue';
import API_Handler from '../router/apiHandler.js'

// Components
import financialTable from '../components/financialTable.vue'
import financialGraph from '../components/financialGraph.vue'

export default defineComponent({
  name: 'QueryView',
  
  data() {
    return {
      API_Handler_Object: null,
      headers: null,
      currentOrdersFiltered: null,
      queryLookupTable: null,
      queryData: null,
      queryURL: null,
    }
  },

  props: {
    query_id: {
      type: Number,
      required: false,
      default: 1
    },
    query_type: {
      type: Number,
      required: true,
      default: 1
    },
    query_start_date: {
      type: String,
      required: false,
      default: "31/12/2024"
    },
    query_end_date: {
      type: String,
      required: false,
      default: "1/12/2024"
    },
    query_is_graph: {
      type: Number,
      required: true,
      default: false
    },
    query_name: {
      type: String,
      required: false,
      default: "-No Name-"
    },
  },
  
  async mounted(){
    // Initialise API hanlding object if it's not created - code is present in all sections that use this object
    if (!this.API_Handler_Object){
      this.API_Handler_Object = new API_Handler()
    }
    
    try{
        // Get query look up table
        this.queryLookupTable = await this.API_Handler_Object.getJSON_QueriesLookupTable()
    }
    catch(ex) {
        console.log("Error getting lookup table: ", ex);
    }

    // Check props were passed
    console.log(this.query_id, this.query_type)

    // Run function with no return - Sets variables inside the function
    this.queryingData()
  },

  components: {
    financialTable,
    financialGraph
  },

  methods:{
    async queryingData(){
      // Initialise API hanlding object if it's not created - code is present in all sections that use this object
      if (!this.API_Handler_Object){
          this.API_Handler_Object = new API_Handler()
      }
      
      // GET the GET url for the query type
      let url = this.queryLookupTable["GET"][this.query_type-1] // queryType start at 1 - index for type starts at 0 (1 == 0)

      let queryDataTemp = null
      try{
          console.log(this.query_start_date, this.query_end_date)

          // GET selected query type - Returns blob object from receiving image for Graph query or returns JSON object from receiving response from Report query
          queryDataTemp = await this.API_Handler_Object.get_ExecuteUserQuery(url, this.query_start_date, this.query_end_date, 1) // Pass user_id as 1 until authention system integration

          console.log(queryDataTemp)
      }
      catch(ex) {
          console.log("Error getting orders: ", ex);
          
          // Turn to null to trigger showing message showing could not get query
          this.headers = null
          this.queryData = null
          this.queryURL = null
          return null
      }

      // Condition also used below to determine which element will render (financialTable.vue or financialGraph.vue)
      if (this.query_is_graph){
          // Download the Image to the browser and provide the URL to display it
          queryDataTemp = URL.createObjectURL(await queryDataTemp.blob())

          if (queryDataTemp){
            this.queryURL = queryDataTemp
          }
          else {
            // Turn to null to trigger showing message showing could not get query
            this.queryURL = null
          }
      }
      else {
          // Get JSON from request as normal
          try{
            queryDataTemp = await queryDataTemp.json()
            console.log(queryDataTemp)
          }
          catch(ex) {
              console.log("Error getting JSON from orders: ", ex);
              
              // Turn to null to trigger showing message showing could not get query
              this.headers = null
              this.queryData = null
              this.queryURL = null
              return null
          }

          if (queryDataTemp){

            // Furthermore resolve headers            
            let headers = []
            for (let key of Object.keys(queryDataTemp[0])){
                // Add vairables to the header as long as they arent nested as the datatable won't render them properly
                if(!(typeof queryDataTemp[0][key] === 'object')){
                    headers.push({
                        title: key.replace("_", " ").split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
                        align: 'start',
                        key: key
                    })
                  }
            }
            this.headers = headers
            this.queryData = queryDataTemp
          }
          else {
            // Turn to null to trigger showing message showing could not get query
            this.headers = null
            this.queryData = null
          }
      }

      return queryDataTemp
    },
  },

  computed: {
    typeID(){
      // Used to check if one of the two or both has been changed so we don't run the change functionality twice
      return [this.query_type, this.query_id]
    }
  },

  watch: {
    async typeID(){      
      // Type and id are used to define a query - when these change the queryData needs to be updated
      await this.queryingData()
    },
  }
});
</script>

<template>
    
  <main class="pt-5">
    <financialTable
    v-if="!query_is_graph && queryData"
    :tableContainerPadding=8
    colour="grey"
    :financialTableData=queryData
    :financialTableHeaders=headers
    :tableTitle=query_name
    :table-height=90
    />

    <financialGraph
    v-else-if="query_is_graph && queryURL"
    :imageURL="queryURL"
    colour="grey"
    :graphContainerPadding=8
    :graphTitle=query_name>
    </financialGraph>

    <div v-if="!queryURL && !queryData">
      <h2>The query returned no data</h2>
    </div>
  </main>
</template>


<style scoped>
</style>