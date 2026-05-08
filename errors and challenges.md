# Error Types & Common Challenges

## 1. Types of Logical Errors

* **Disjoint properties between the same pair of entities**
    * **1.1. Disjointness between two properties:** Fails; requires at least `sh:disjoint` to be fixed.
    * **1.2. Disjointness between a property and a property chain:** Fails; can be fixed with custom rules (see [Rule 1](#uncle-inference-shape)).
* **Disjoint classes assigned to the same entity:** Fails; can be fixed with [Rule 4](#class-disjointness).
* **Violation of domain or range constraints:** Passes, but class hierarchy must be considered (see Challenge 1.1).
* **Irreflexivity Violation:** A property is `owl:IrreflexiveProperty`, but data contains triple $(A, P, A)$.
    * *Result:* Fails; requires custom rules.
* **Asymmetry Violation:** $(A, P, B)$ and $(B, P, A)$ both exist for an `owl:AsymmetricProperty`.
    * *Result:* Fails; requires custom rules to handle.
* **Max Cardinality Violation:** A node has 3 values for a property restricted to `maxQualifiedCardinality 2`.
    * *Result:* Passes.
* **Functional Property Violation:** A `FunctionalProperty` (e.g., `hasBirthMother`) points to two distinct individuals.
    * *Result:* Passes; requires custom rules.

---

## 2. Common Challenges

### 1. Class Hierarchy
* **1.1. Range constraints:** If `sh:range :Person`, then `:Man` at the end of the property (subclass of `:Person`) will still fail SHACL validation. (Fixed with [Rule 2](#superclass-inference)).
* **1.2. Inheritance:** Constraints should be inherited down the hierarchy - for the ontology to handlef

### 2. Property Shapes Propagation
* `:Man` should inherit all property shapes from `:Person` and parallel shapes like `:Ancestor` (if not disjoint).

### 3. Constraint Expansion
* For constraints like `sh:disjoint`, every original property as well as its children and equivalents must be explicitly listed.

### 4. Inverse Property Handling
* **4.1. Domain/Range:** Protege shows correct inferrals, but exports often lack the inferred domain/range even with all checkboxes marked.
* **4.2. propertyDisjointWith:** Not inferred by reasoners; likely needs explicit specification in the ontology.
* **4.3. propertyChainAxiom:** Inverse triples must be inferred dynamically (see [Rule 3](#dynamic-inverse-shape)), otherwise chains stated in inverses won't be recognized.

---

## 3. Implementation Rules (SHACL)

### Uncle Inference Shape
```turtle
:UncleInferenceShape
    a sh:NodeShape ;
    sh:targetSubjectsOf :isBrotherOf ;
    sh:rule [
        a sh:TripleRule ;
        sh:subject sh:this ;
        sh:predicate :isUncleOf ;
        sh:object [
            sh:path ( :isBrotherOf :hasChild )
        ] ;
    ] .
```

### Superclass Inference
```turtle
:Woman a sh:NodeShape,
        rdfs:Class ;
    sh:rule [
        a sh:TripleRule ;
        sh:subject sh:this ;
        sh:predicate rdf:type ;
        sh:object :Person ;
    ] .
```

### Dynamic Inverse Shape
```turtle
:DynamicInverseShape
    a sh:NodeShape ;
    sh:targetClass rdfs:Resource ;
    sh:rule [
        a sh:SPARQLRule ;
        sh:construct """
            CONSTRUCT {
                ?o ?inv $this .
            }
            WHERE {
                # 1. Find any property ?p connected to the current node
                $this ?p ?o .
                
                # 2. Find the inverse property definition in the metadata
                { ?p owl:inverseOf ?inv . }
                UNION
                { ?inv owl:inverseOf ?p . }
                
                # 3. Optimization: avoid literal subjects
                FILTER (isIRI(?o))
            }
        """ ;
    ] .
```

### Class Disjointness
```turtle
:ManDisjointnessShape
    a sh:NodeShape ;
    sh:targetClass :Man ;
    # Violation if the node is also a Woman
    sh:not [
        sh:class :Woman ;
    ] ;
    sh:message "A node cannot be both a Man and a Woman." .
```