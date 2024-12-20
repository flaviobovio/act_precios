<template>
  <Page class="page">
    <ActionBar class="actionbar">
      <StackLayout>
        <FlexboxLayout flexDirection="row" justifyContent="space-between">
          <label text="Actualizador de Precios" class="applabel"/>
          <button class="far" text.decode="&#xf185;"  style="font-size: 20px;" @tap="configApp" />
        </FlexboxLayout>
        <FlexboxLayout flexDirection="row" justifyContent="space-between">
          <label text="by 30vio" class="vendorlabel"/>
          <label v-if="backend" :text="'Servidor ' + backend" class="vendorlabel"/>
        </FlexboxLayout>
      </StackLayout>
    </ActionBar>
    <StackLayout class="form">

      <Label text="Escanear o ingresar código de barra" class="label" />
      <FlexboxLayout class="button-row" flexDirection="row" justifyContent="space-between">
        <Button class="code-button fas" text.decode="&#xf02a;" @tap="scanBarcode" />         
        <Button class="code-button far" text.decode="&#xf11c;" @tap="typeBarcode" />
      </FlexboxLayout>
      
      <Label text="" />

      <StackLayout v-if="scannedResult" class="info-section">
        <Label text="Código de Barra" class="label" />
        <Label :text="scannedResult" class="value" />
      </StackLayout>

      <StackLayout v-if="apiResponse" class="info-section">
        <Label text="Registro" class="label" />
        <Label :text="apiResponse.registro" class="value" />
        
        <Label text="Descripción" class="label" />
        <Label :text="apiResponse.descripcion" class="value" />
        
        <Label text="Precio" class="label" />
        <Label :text="`$${apiResponse.precio}`" class="value" />
      </StackLayout>

      <StackLayout v-if="apiResponse" class="update-section">     
        <TextField
          v-model="updatedPrice"
          keyboardType="number"
          hint="Ingrese nuevo precio"
          class="input large-input"
        />
        <Button
          text="Actualizar Precio"
          :isEnabled="!!updatedPrice"
          @tap="updatePrice(apiResponse.registro, updatedPrice)"
          class="update-button"
        />      



      </StackLayout>
    </StackLayout>
  </Page>
</template>

<script>
import { BarcodeScanner } from "@nstudio/nativescript-barcodescanner";
import { FlexboxLayout, prompt, StackLayout } from "@nativescript/core";
import configManager from "../utils/configManager"
import toastMessage from "~/utils/toastMessage";


export default {
  data() {
    return {
      scannedResult: null,
      apiResponse: null,
      updatedPrice: "",
      barcodeScanner: new BarcodeScanner(),
      backend: configManager.loadConfig()['backend'], 
    };
  },

  methods: {

    async scanBarcode() {
      try {
        const result = await this.barcodeScanner.scan({
          formats: "QR_CODE, EAN_13",
          cancelLabel: "Detener",
          message: "<Escanee un código>",
          showFlipCameraButton: true,
          showTorchButton: true,
          orientation: "landscape",
        });

        if (result?.text) {
          this.scannedResult = result.text;
          await this.fetchProductInfo(result.text);
        } else {
          toastMessage.warning('No se ha escaneado código')
        }
      } catch (error) {
        toastMessage.error('Error:', error);
      }
    },

    async typeBarcode() {
      try {
        const inputOptions = {
          title: "Ingresar Código",
          message: "Por favor ingrese el código de barras",
          inputType: "number",       
          okButtonText: "Aceptar",
          cancelButtonText: "Cancelar",
        };

        const result = await prompt(inputOptions);

        if (result.result && result.text) {
          this.scannedResult = result.text;
          await this.fetchProductInfo(result.text);
        } else {
          toastMessage.warning("Ingreso por teclado cancelado");
        }
      } catch (error) {
        toastMessage.error("Error:", error);
      }
    },

    async fetchProductInfo(codigo) {
      try {
        const url = `http://${this.backend}/buscar/${codigo}`;
        const response = await fetch(url);
        if (!response.ok) {
          toastMessage.error("Error:", response.statusText);
          return;
        }

        const data = await response.json();

        if (data.status === "Not found") {
          this.apiResponse = null;
          toastMessage.warning("Producto no encontrado.");
        } else {
          this.apiResponse = data;
        }
      } catch (error) {
        toastMessage.error("Error al leer datos del producto");
      }
    },

    async updatePrice(registro, nuevoPrecio) {
 
 
      try {
        // Check if the updatedPrice is empty
        const precio = parseFloat(nuevoPrecio).toFixed(2)
        if (isNaN(precio) || precio <= 0) {
          toastMessage.warning("Ingrese precio nuevamente");
          return;
        }

        const url = `http://${this.backend}/cambiar/${registro}/${precio}`;

        const response = await fetch(url, {
          method: "PUT",
        });



        if (!response.ok) {
          toastMessage.error("Error al actualizar el precio");
          return;
        }

      const result = await response.json();

      if (result.status === "success") {
        toastMessage.info("Precio actualizado exitosamente");
        this.apiResponse.precio = nuevoPrecio;
        this.updatedPrice = ""; 
      } else {
        toastMessage.error(result.message || "Error al actualizar el precio");
      }
      } catch (error) {
        toastMessage.error("Error al actualizar el precio");
      } 
 
    },



    async configApp() {

      try {
        const inputOptions = {
          title: "Servidor y puerto",
          message : 'Ingrese <servidor>:<puerto> Ej: "192.168.1.1:8080"', 
          inputType: "text",
          okButtonText: "Aceptar",
          cancelButtonText: "Cancelar",
          defaultText: this.backend,           
        };

        const result = await prompt(inputOptions);

        if (result.result && result.text) {

          const config = {
            backend: result.text,
            token: ""
          };
          configManager.saveConfig(config);
          toastMessage.warning('Reinicie la aplicación')
        }
      } catch (error) {
        toastMessage("Error:", error);
      }
    },

  },
};
</script>

<style scoped>
.page {
  background-color: whitesmoke;
}
.form {
  padding: 20;
}

.actionbar {
  background-color: rgb(13, 37, 55);
}

.applabel {
  text-align: right;
  font-size: 18px;
  font-weight: bold;
}

.vendorlabel {
  text-align:right;
  vertical-align: bottom;
  font-size: 10px;
  font-style: italic;
}


/* Sección de información */
.info-section {
    margin-bottom: 16px;
    align-items: center;    
}

/* Estilos para etiquetas */
.label {
    font-size: 16px;
    color: #333;
}

/* Estilos para valores */
.value {
    font-size: 18px;
    font-weight: bold;
    color: #000;
    margin-bottom: 8px;
}



/* Campo de entrada */
.input {
    margin-top: 8px;
    padding: 8px;
    font-size: 18px;
    font-weight: bold;
    font-style: italic;    
    border: 1px solid #ccc;
    border-radius: 4px;
    text-align: center;
}

/* Contenedor de botones en la misma línea */
.button-row {
    width: 100%;
    justify-content: space-between;
}



.code-button {
  flex: 1; /* Ambos botones ocupan el mismo espacio */
  margin: 0 8px; /* Espaciado uniforme entre botones */  
  /* flex-grow: 1;
  flex-basis: 45%;
  margin: 0 5px; */
  margin-top: 10px;
  background-color: rgb(13, 37, 55);
  color: white;
  border-radius: 16px;
  font-size: 16px;
}
.update-button {
  margin-top: 10px;
  background-color: green;
  color: white;
  border-radius: 8px;
}


.far {
  font-family: "Font Awesome 6 Free", "fa-regular-400";
  font-weight: 400;
  font-size: 36; /* Adjust the font size */
  color: white; /* Adjust the color */
  background-color: rgb(13, 37, 55);  
}


.fas {
  font-family: "Font Awesome 6 Free", "fa-solid-900";
  font-weight: 400;
  font-size: 36; /* Adjust the font size */
  color: white; /* Adjust the color */
  background-color: rgb(13, 37, 55);  

}



</style>
