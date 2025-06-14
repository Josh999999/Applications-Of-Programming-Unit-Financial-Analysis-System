<script>
export default {
  data() {
    return {
    }
  },
  props: {
    imageURL:{
      type: String,
      required: true,
    },
    colour: {
      type: String,
      required: false,
      default: "grey"
    },
    graphContainerPadding: {
      type: Number,
      required: false,
      default: 0
    },
    graphTitle: {
      type: String,
      required: false,
      default: "Financial graph"
    }
  },
  async mounted(){

  },
  computed: {
    graphContainerPaddingString(){
      // Create vuetiy classifiers for adding margin to the right and left of the container
      return "pl-" + String(this.graphContainerPadding) + " pr-" + String(this.graphContainerPadding)
    },
    
    graphContainerClassBinding(){
      // Returns all class bindings together - Only padding currently available
      return this.graphContainerPaddingString
    }
  }
} 
</script>

<template>
  <div
    class="truegraphContainerDiv"
    :class="graphContainerClassBinding">
    <div 
      class="graphContainerDiv" 
      :style="{ backgroundColor: colour }">
      <h3 class="graphTitle">{{ graphTitle }}</h3>

      <v-divider 
        class="graphDivider"
        :dark=true
      ></v-divider>

      <img width="1700" height="1000" :src="imageURL"></img>
    </div>
  </div>
</template>

<style scoped>
.graphTitle{
  color: black;
}

.graphDivider{
  width: 100%;
  margin-top: 1vh;
  margin-bottom: 1vh;
}

.truegraphContainerDiv{
  width: 100%;
}

.graphContainerDiv{
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  align-items: center;
  width: 100%;
  border-radius: 45px;
  padding-top: 1vh;
  padding-left: 1vh;
  padding-right: 1vh;
  padding-bottom: 3vh;
  overflow: hidden;
}
</style>