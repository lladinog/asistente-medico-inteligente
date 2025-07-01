# 📁 Carpeta de Datos de Prueba

Esta carpeta contiene archivos de prueba para el sistema de asistentes médicos inteligentes.

## 📂 Estructura

```
data/
├── pdfs/          # Archivos PDF de exámenes médicos
├── txt/           # Archivos de texto con resultados de exámenes
└── README.md      # Este archivo
```

## 📄 Archivos de Texto Disponibles

### `txt/hemograma.txt`
- **Tipo**: Hemograma completo
- **Contenido**: Resultados de análisis de sangre con valores anormales
- **Hallazgos**: Anemia leve, leucocitosis, neutrofilia

### `txt/quimica_sanguinea.txt`
- **Tipo**: Química sanguínea completa
- **Contenido**: Perfil metabólico con múltiples alteraciones
- **Hallazgos**: Insuficiencia renal leve, dislipidemia, hiperuricemia

### `txt/tiroides.txt`
- **Tipo**: Perfil tiroideo
- **Contenido**: Hormonas tiroideas y anticuerpos
- **Hallazgos**: Hipotiroidismo subclínico, tiroiditis autoinmune

## 📋 Cómo Usar

### Para Probar con Archivos de Texto
1. Los archivos en `txt/` se procesan automáticamente al ejecutar:
   ```bash
   python agents/interpretacionExamenes.py
   ```

### Para Probar con PDFs
1. Coloca archivos PDF de exámenes médicos en la carpeta `pdfs/`
2. Nombres sugeridos:
   - `examen.pdf`
   - `hemograma.pdf`
   - `quimica.pdf`
   - `tiroides.pdf`

### Agregar Nuevos Archivos
1. **Para texto**: Crea archivos `.txt` en `data/txt/`
2. **Para PDFs**: Coloca archivos `.pdf` en `data/pdfs/`
3. Los archivos deben contener resultados de exámenes médicos reales o simulados

## 🔍 Formato Esperado

### Archivos de Texto
- Deben contener resultados de exámenes médicos
- Incluir valores, rangos normales y observaciones
- Formato libre pero estructurado

### Archivos PDF
- Deben ser documentos médicos escaneados o digitales
- Contener resultados de laboratorio o imágenes médicas
- El sistema extraerá automáticamente el texto

## ⚠️ Notas Importantes

- Los archivos de prueba son simulados para fines de desarrollo
- No contienen información médica real de pacientes
- El sistema está diseñado para procesar cualquier formato de examen médico
- Los resultados del análisis son generados por IA y no reemplazan la evaluación médica profesional 