<script>
import { defineComponent } from 'vue';
import API_Handler from '../router/apiHandler.js'

export default defineComponent({
  name: 'CreateQueryFormView',
  
  data() {
    return {
      API_Handler_Objectect: null,
      postQueryRoute: null,
      queryStartDate: null,
      queryEndDate: null,
      queryName: null,
      queryNameRules: [
        v => !!v || 'The Query name is required',
        v => (v && v.length <= 20) || 'The Query name must be 20 characters or less',
      ],
      queryLookupTable: null
    }
  },

  props:{
    queryType: {
      type: Number,
      required: true,
    },
    colour: {
      type: String,
      required: false,
      default: "grey"
    },
    formTitle: {
      type: String,
      required: false,
      default: "Create query"
    },
    tableHeight: {
      type: Number,
      required: false,
      default: 50
    },
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

    // GET POST route from type of query via query lookup object returned from route
    this.postQueryRoute = (await this.queryLookupTable)["POST"][this.queryType - 1] // queryType start at 1 - index for type starts at 0 (1 == 0)
  },

  
  methods: {
    async validate () {
      // validate the all inputs - Can't validate dates either (may have to add code but date selector should restrict input enough)
      const { valid } = await this.$refs.form.validate()

      if (valid) alert('Form is valid')
    },

    reset () {
      // Reset all variables bound to inputs in the form to their original values
      this.$refs.form.reset()

      // Can't reach the date selectors through the form
      this.queryStartDate = null
      this.queryEndDate = null
    },
  },
  
  watch: {
    async queryType(){
      // Get the query types post route from the lookup table
      this.postQueryRoute = (await this.queryLookupTable)["POST"][this.queryType - 1] // queryType start at 1 - index for type starts at 0 (1 == 0)
      this.reset()
    }
  }
});
</script>

<template>
    <template v-if="queryType !== null">
      <div class="trueFormContainerDiv">
        <div 
          class="formContainerDiv" 
          :style="{ backgroundColor: colour, height: String(tableHeight) + 'vh' }">
          <h3 
            class="formTitle">
            Create Query: {{ formTitle }}
          </h3>

          <v-form 
            ref="form" 
            class="createQueryFormElement">
            <div class="nameFormSection">
              <h3 
                class="mt-6">
                Text Input section
              </h3>

              <v-divider class="mb-2 pr-1"></v-divider>       

              <v-text-field
                v-model="queryName"
                label="Query Name"
                :counter="20"
                :rules="queryNameRules"
                required
              ></v-text-field>
            </div>

            <div class="dateFormSection">
              <h3 
                class="mt-6">
                Date selection section
              </h3>

              <v-divider class="mb-2"></v-divider>          

              <v-container>
                <v-row justify="space-around">
                  <v-date-picker
                    v-model="queryStartDate"
                    color="primary"
                  ></v-date-picker>
                </v-row>
              </v-container>

              <v-container>
                <v-row justify="space-around">
                  <v-date-picker
                    v-model="queryEndDate"
                    color="primary"
                  ></v-date-picker>
                </v-row>
              </v-container>
            </div>
          </v-form>
        </div>    

        <div class="formButtonContainer">
          <v-btn
            class="mt-4"
            color="success"
            block
            @click="validate"
          >
            Save
          </v-btn>

          <v-btn
            class="mt-4"
            color="error"
            block
            @click="reset"
          >
            Cancel
          </v-btn>
        </div>
      </div>
    </template>
</template>


<style scoped>
.v-date-picker{
  display: flex;
  width: 100%;
  height: 45vh;
}

.formTitle{
  color: black;
}

.trueFormContainerDiv{
  width: 100%;
  display: flex;
  flex-direction: column;
}

.dateFormSection{
  width: 50%;
  height: 100%;
}

.nameFormSection{
  width: 50%;
}

.createQueryFormElement{
  display: flex;
  flex-direction: row;
  width: 100%;
}

.formContainerDiv{  
  overflow-y: scroll;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  border-radius: 45px;
  padding-top: 1vh;
  padding-left: 1vh;
  padding-right: 1vh;
}
</style>