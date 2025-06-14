<script setup>
import API_Handler from '../router/apiHandler.js'
</script>

<script>
export default {
  data() {
    return {
    }
  },
  props: {
    financialTableData:{
      type: Array,
      required: true,
    },
    financialTableHeaders:{
      type: Array,
      required: true,
    },
    tableContainerPadding: {
      type: Number,
      required: false,
      default: 0
    },
    colour: {
      type: String,
      required: false,
      default: "grey"
    },
    tableTitle: {
      type: String,
      required: false,
      default: "Financial Table"
    },
    tableHeight: {
      type: Number,
      required: false,
      default: 50
    }
  },
  async mounted(){

  },
  computed: {
    tableContainerPaddingString(){
      // Create vuetiy classifiers for adding margin to the right and left of the container
      return "pl-" + String(this.tableContainerPadding) + " pr-" + String(this.tableContainerPadding)
    },

    tableContainerClassBinding(){
      // Returns all class bindings together - Only padding currently available
      return this.tableContainerPaddingString
    },
    
    innerTableHeight(){
      /* 
        Table height attribute is about 8 times the vh metric used for the height of the 
        .tableContainer div used to contain the table the table
      */
      return this.tableHeight * 8
    }
  }
} 
</script>

<template>
  <div
    class="trueTableContainerDiv"
    :class="tableContainerClassBinding">
    <div 
      class="tableContainerDiv" 
      :style="{ backgroundColor: colour, height: String(tableHeight) + 'vh' }">
      <h3 class="tableTitle">{{ tableTitle }}</h3>

      <v-divider 
        class="tableDivider"
        :dark=true
      ></v-divider>

      <v-data-table-virtual
        :style="{ backgroundColor: colour}"
        :headers="financialTableHeaders"
        :items="financialTableData"
        :height=innerTableHeight
        item-value="name"
        :color="colour"
      ></v-data-table-virtual>
    </div>
  </div>
</template>

<style scoped>
.tableTitle{
  color: black;
}

.tableDivider{
  width: 100%;
  margin-top: 1vh;
  margin-bottom: 1vh;
}

.trueTableContainerDiv{
  width: 100%;
}

.tableContainerDiv{
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  align-items: center;
  width: 100%;
  border-radius: 45px;
  padding-top: 1vh;
  padding-left: 1vh;
  padding-right: 1vh;
  overflow: hidden;
}

.v-data-table-virtual{
  flex-shrink: 0; 
  width: 100%;
}
</style>