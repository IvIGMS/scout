package com.ivanfrias.Scout.controllers;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import com.ivanfrias.Scout.models.RequestData;

import java.io.BufferedReader;
import java.io.IOException; 
import java.io.InputStreamReader;

@RestController
public class ScoutController {
    @PostMapping("/submitData")
    public ResponseEntity<String> submitData(@RequestBody RequestData requestData) {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("bash", "-c", "source ../python/env/bin/activate && python3 ../python/scripts/main.py " + requestData.getUsername() + " " + requestData.getUrl());
            processBuilder.redirectErrorStream(true); // Redirigir errores a la salida estándar
            Process process = processBuilder.start(); 

            // Leer la salida del script
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }

            int exitVal = process.waitFor();
            if (exitVal == 0) {
                // El script se ejecutó correctamente
                return ResponseEntity.ok("Resultado del script: " + output.toString());
            } else {
                // Algo salió mal
                return ResponseEntity.badRequest().body("Error al ejecutar el script de Python");
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().body("Error al ejecutar el script de Python");
        }
    }
}