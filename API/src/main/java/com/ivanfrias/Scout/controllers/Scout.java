package com.ivanfrias.Scout.controllers;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import com.ivanfrias.Scout.models.RequestData;
import java.io.File;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

@RestController
public class Scout {
    @PostMapping("/submitData")
    public ResponseEntity<String> submitData(@RequestBody RequestData requestData) {
        String pythonScriptPath = "C:\\Users\\Ivan Frias\\Documents\\proyectos\\scout\\scripts\\prueba.py"; // Asegúrate de reemplazar esto con la ruta real de tu script
        String pythonExecutable = "python"; // O "python3", dependiendo de cómo accedas a Python en tu sistema

        try {
            ProcessBuilder processBuilder = new ProcessBuilder(pythonExecutable, pythonScriptPath);
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
            return ResponseEntity.internalServerError().body("Error al ejecutar $$$$$$$$$$$$$$$$$$ el script de Python");
        }
    }
}
