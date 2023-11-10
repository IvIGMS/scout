package com.ivanfrias.Scout.controllers;

import java.util.ArrayList;
import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
    @GetMapping(value = "/show/{username}")
    public ResponseEntity<List<String>> getUserRows(@PathVariable("username") String username) {
        List<String> list = new ArrayList<>();
        list.add("Manzanas");
        list.add("Fresas");
        list.add("Platanos");
        list.add(username);
        return ResponseEntity.ok(list);
    }
}