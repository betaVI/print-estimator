// import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Spinner from './components/Spinner.vue'
import Alert from './components/Alert.vue'
import ListView from './components/ListView.vue'
import EditView from './components/EditView.vue'
import FileImport from './components/FileUploader.vue'

const app = createApp(App);

app.component('Spinner', Spinner);
app.component('Alert', Alert);
app.component('ListView', ListView)
app.component('EditView', EditView)
app.component('FileImport', FileImport)

app.use(router);

app.mount('#app');
