<script>
import { defineComponent } from 'vue';

// Components
import API_Handler from '../router/apiHandler.js'
import CreateQueryFormView from './CreateQueryFormView.vue';

export default defineComponent({
  name: 'CreateQueryView',
  
  data() {
    return {
      API_Handler_Object: null,
      queryNames: null,
      selectedQueryType: null,
      selectedQueryName: null,
      queryLookupTable: null,
    }
  },
  
  async mounted(){
    // Initialise API hanlding object if it's not created - code is present in all sections that use this object
    if (!this.API_Handler_Object){
      this.API_Handler_Object = new API_Handler()
    }
    
    try{
        // GET query look up table
        this.queryLookupTable = await this.API_Handler_Object.getJSON_QueriesLookupTable()
    }
    catch(ex) {
        console.log("Error getting lookup table: ", ex);
    }

    // GET name of the types of queries via query lookup object returned from route
    this.queryNames = (await this.queryLookupTable)["queryNames"]

    console.log(this.queryNames)
  },

  components: {
    CreateQueryFormView
  },

  methods: {
    newQueryTypeClickedHandler(queryIndex){
      // Update selected query type information
      this.selectedQueryType = queryIndex; 
      this.selectedQueryName = this.queryNames[queryIndex]
    }
  }
});
</script>

<template>
    <v-layout>
      <v-navigation-drawer 
        theme="dark"
        permanent
      >
        <h2 class="ml-2 mt-3">Select Query Type</h2>

        <v-list nav>
          <template
            v-if="queryNames"
            v-for="(queryName, i) in queryNames"
            :key="i">
              <v-list-item
                nav
                style="padding: 0%;"
                :value="queryName"
                @click="newQueryTypeClickedHandler(i)"
              >
                <div
                  class="queryTypeInfoContainer">
                  <v-icon
                    size="35"
                    class="pl-1"
                    color="green"
                  >
                    mdi-plus
                  </v-icon>
                  
                  <v-list-item-title 
                    v-text="queryName"
                    class="pl-3"
                    color="white">
                  </v-list-item-title>
                </div>
              </v-list-item>
          </template>
        </v-list>
      </v-navigation-drawer>
      
      <v-main class="mt-5 ml-5 mr-5">
        <template v-if="selectedQueryType !== null">
           <CreateQueryFormView
            color="grey"
            :tableHeight="80"
            :queryType=Number(selectedQueryType)
            :formTitle=selectedQueryName>
           </CreateQueryFormView>
        </template>
      </v-main>
    </v-layout>
</template>


<style scoped>
.queryTypeInfoContainer{
  display: flex;
  flex-direction: row;
  align-items: center;
}

.navigation-drawer {
  padding-right: 1vh;
}

.v-layout{
  height: 100%;
  display: flex;
  grid-column: 1;
}
</style>