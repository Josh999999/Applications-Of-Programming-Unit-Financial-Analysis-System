<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<script>
import { defineComponent } from 'vue';

// Components
import API_Handler from './router/apiHandler.js'

export default defineComponent({
  name: 'AppVue',
  
  data() {
    return {
      API_Handler_Object: null,
      queries: null,
      queryLookup: null,
    }
  },
  
  async mounted(){
    // Initialise API hanlding object if it's not created - code is present in all sections that use this object
    if (!this.API_Handler_Object){
      this.API_Handler_Object = new API_Handler()
    }

    try{
        // GET query look up table
        this.queryLookup = await this.API_Handler_Object.getJSON_QueriesLookupTable()
    }
    catch(ex) {
        console.log("Error getting lookup table: ", ex);
        return null
    }

    // GET list of all users queries to display
    this.queries = await this.API_Handler_Object.getJSON_UserQueries(1)
  },

  methods: {
    async deleteQuery(queryId, queryType){
      // Initialise API hanlding object if it's not created
      if (!this.API_Handler_Object){
        this.API_Handler_Object = new API_Handler()
      }

      // Get DELETE for route for query type
      let url = (await this.queryLookup)["DELETE"][queryType-1]

      let queryData = ""
      try{
          // DELETE selected query with given id of given type (via url)
          let queryData = await this.API_Handler_Object.delete_ExecuteUserQuery(url, queryId, 1) // user_id given as 1 until integration with authentication system
      }
      catch(ex) {
          console.log("Error getting orders: ", ex);
          return null
      }

      console.log("Delete message: ", queryData);

      // Update query list data - list will likely change after DELETE statement goes through
      // GET list of all users queries to display
      this.queries = await this.API_Handler_Object.getJSON_UserQueries(1)

      // Deal with removal of a query
      if (this.queries[0]){
        // Force back to top query in the list - display first query in the list after deletion
        let firstQuery = this.queries[0]

        // Using RouterLink we pass these parameters as props to the component (QueryView component)
        let routelink = '/query?queryId=' + firstQuery['id'] 
          + '&queryName=' + firstQuery['name'] 
          + '&queryType=' + firstQuery['type'] 
          + '&queryEndDate=' + firstQuery['end_date'] 
          + '&queryStartDate=' + firstQuery['start_date'] 
          + '&queryIsGraph=' + firstQuery['isGraph']

        // Replacing path adds no new history
        this.$router.replace(routelink);
      }
      else{
        // If no querys left force back to homepage
        this.$router.replace("/");
      }
    },
  }
});

</script>

<template>
  <v-app>
    <v-navigation-drawer 
      theme="dark"
      permanent
      rail
      app 
    >
      <v-list nav>
        <v-list-item
          nav
          style="padding: 0%;"
        >
          <v-icon
            size="35"
          >
            mdi-account-star
          </v-icon>
        </v-list-item>
      </v-list>

      <v-list
        density="compact"
        nav
      >
        <v-list-item 
          prepend-icon="mdi-view-dashboard" 
          value="dashboard">
        </v-list-item>

        <v-list-item 
          prepend-icon="mdi-cog" 
          value="messages">
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-navigation-drawer 
      class="navigation-drawer"
      width="500"
      permanent
      style="background-color: lightgrey"
      app
    >
      <v-list-item 
        class="mainListItem"
        style="
          border-top: 1px solid rgba(0, 0, 0, 0.4);
          border-bottom: 1px solid rgba(0, 0, 0, 0.4);
          padding-top: 4%;
          padding-bottom: 4%;
        "
      >
        <RouterLink 
          to="/" 
          class="router"
        >
          <h1 class="mainNavigationHeader">Home</h1>
        </RouterLink>
      </v-list-item>

      <v-list-item
        class="mainListItem"
        style="
          border-top: 1px solid rgba(0, 0, 0, 0.4);
          border-bottom: 1px solid rgba(0, 0, 0, 0.4);
          padding-top: 4%;
          padding-bottom: 4%;
        "
      >
        <RouterLink 
          to="/createQuery" 
          class="router"
        >
          <h1 class="mainNavigationHeader">Create New Query</h1>
        </RouterLink>
      </v-list-item>
  
      <h2 class="userQueriesHeader">User queries</h2>
      
      <v-list
        :lines="false"
        density="compact"
        nav
        class="queryList"
        id="mainQueryList"
      >
        <template
            v-if="queries"
            v-for="(query, i) in queries"
            :key="i">
            <div
              class="queryListItemContainer">
              <RouterLink
                :to="'/query?queryId=' + query['id'] 
                  + '&queryName=' + query['name'] 
                  + '&queryType=' + query['type'] 
                  + '&queryEndDate=' + query['end_date'] 
                  + '&queryStartDate=' + query['start_date'] 
                  + '&queryIsGraph=' + query['isGraph'] "
                class="queryRoute"
                replace>

                  <v-list-item
                    :value="query"
                    color="primary"
                    class="queryListItem">

                    <v-list-item-title class="queryItemText">
                      <h3>{{query.name}}</h3>
                    </v-list-item-title>
                  </v-list-item>
                                
              </RouterLink>

              <v-list-item 
                class="queryItemIcon"
                :value="i"
                @click="deleteQuery(query['id'], query['type'])">
                <v-icon
                  size="35"
                  class="pl-1"
                  color="red"
                >
                  mdi-delete
                </v-icon>
              </v-list-item>            
            </div>
          </template>
      </v-list>
    </v-navigation-drawer>

    <v-main class="routerContainer">
      <RouterView/>
    </v-main>
  </v-app>
</template>

<style>
.queryItemIcon{
  color: red;
}

.queryItemText{
  display: flex;
  color: black;
}

.queryDeleteIcon{
  float: right;
}

.queryListItem{  
  display: flex;
  flex-direction: row;
  width: 100%;
}

.queryRoute{
  display: flex;
  width: 100%;
}

.queryListItemContainer{
  display: flex;
  flex-direction: row;
}

.queryList{
  margin-left: 11%;
  display: flex;
  flex-direction: column;
}

.userQueriesHeader{
  margin-top: 3vh;
  margin-left: 8%;
}

.mainListItem{
  margin-left: 5%;
  padding: 0%;
  margin-top: 8%;
}

.mainNavigationHeader{
  margin-left: 11%;
}

.navigation-drawer {
  padding-right: 1vh;
}

.v-layout{
  height: 100%;
  display: flex;
}

.routerContainer{
  display: flex;
}
</style>
