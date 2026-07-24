================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
The Duchess of Montpensier


The Count of ÉvreuxThe Countess of Évreux


Princess Béatrice


The Duke of OrléansThe Duchess of Orléans


The Dowager Countess of La Marche


The Countess of Schönborn-Buchheim


Princess Hélène, Countess of Limburg Stirum


The Dowager Duchess of Calabria


The Dowager Duchess of Württemberg


Princess Claude, Mrs. Gandolfi


Princess Chantal, Baroness of Sambucy de Sorgue


Charles Philippe Marie Louis d'Orléans (born 3 March 1973) is a member of the House of Orléans.
He is the elder of two sons of Prince Michel d'Orléans and his former wife Béatrice Pasquier de Franclieu.
His paternal grandfather was Prince Henri d'Orléans, the Orléanist pretender to the French throne.
The couple's only child, Princess Isabelle d'Orléans, was born on 22 February 2012 in Lisbon, Portugal.
Her godparents are Princess Maria Theodora zu Löwenstein-Wertheim-Freudenberg and Felipe VI of Spain (then Prince of Asturias).
Charles-Philippe and Naomi-Valeska's child, Princess Élisabeth Victoire Jeanne Marie d'Orléans, was born on 15 April 2026 in Monaco.
His acceptance of this role placed the order under the sanction of a dynastic prince of the House of Bourbon, in what is said to be a continuation of a tradition established since the 13th century when the Order of Saint Lazarus came under the protection of King Philippe le Bel.
Title controversy

On 8 December 2004, he received the title "Duke of Anjou" from his uncle Prince Henri d'Orléans, head of the House of Orléans.
There is some controversy in the use of this title by an Orléans prince.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (d7e9379a-3f82-4bd7-9401-81fc948f2442)
 Call ID: d7e9379a-3f82-4bd7-9401-81fc948f2442
  Args:
    type: :Man
    source: Charles_Philippe_Marie_Louis_dOrleans
  AssignClass (2b449c13-7304-4ecc-b8a9-6b0a5329729a)
 Call ID: 2b449c13-7304-4ecc-b8a9-6b0a5329729a
  Args:
    source: Charles_Philippe_Marie_Louis_dOrleans
    type: :Person
  AddLiteral (0805b8d4-7eb8-4346-8396-58bf83dbe0b1)
 Call ID: 0805b8d4-7eb8-4346-8396-58bf83dbe0b1
  Args:
    literal_value: 1973
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Charles_Philippe_Marie_Louis_dOrleans
  AssignClass (4aa77aa1-fb56-450c-b623-308d965c507b)
 Call ID: 4aa77aa1-fb56-450c-b623-308d965c507b
  Args:
    source: Michel_dOrleans
    type: :Man
  AssignClass (4f993e5e-136b-4d80-862f-c3394935c79c)
 Call ID: 4f993e5e-136b-4d80-862f-c3394935c79c
  Args:
    source: Michel_dOrleans
    type: :Person
  AssignClass (2631c5f7-a343-482a-9717-8a2f56c5da10)
 Call ID: 2631c5f7-a343-482a-9717-8a2f56c5da10
  Args:
    source: Beatrice_Pasquier_de_Franclieu
    type: :Woman
  AssignClass (150f11ce-0e17-4668-8c64-654900cbeb85)
 Call ID: 150f11ce-0e17-4668-8c64-654900cbeb85
  Args:
    type: :Person
    source: Beatrice_Pasquier_de_Franclieu
  AddTriple (6e9cad66-90a8-4cdb-b63e-933f8fc7f169)
 Call ID: 6e9cad66-90a8-4cdb-b63e-933f8fc7f169
  Args:
    source: Charles_Philippe_Marie_Louis_dOrleans
    target: Michel_dOrleans
    relation: :hasFather
  AddTriple (87902c5c-08be-4a4d-a884-0b79bd5a6f4e)
 Call ID: 87902c5c-08be-4a4d-a884-0b79bd5a6f4e
  Args:
    relation: :hasMother
    target: Beatrice_Pasquier_de_Franclieu
    source: Charles_Philippe_Marie_Louis_dOrleans
  AssignClass (5d4a717e-a9b1-4e2b-ad47-719f5493b03e)
 Call ID: 5d4a717e-a9b1-4e2b-ad47-719f5493b03e
  Args:
    source: Henri_dOrleans
    type: :Man
  AssignClass (2bd55299-ac4f-4afa-a238-8d5dcc13fa33)
 Call ID: 2bd55299-ac4f-4afa-a238-8d5dcc13fa33
  Args:
    source: Henri_dOrleans
    type: :Person
  AddTriple (12e58627-c04d-4042-ad64-e274353f840e)
 Call ID: 12e58627-c04d-4042-ad64-e274353f840e
  Args:
    source: Michel_dOrleans
    relation: :hasFather
    target: Henri_dOrleans
  AssignClass (8afdaf9d-2b1a-4b2f-96cb-76fb36a1fa29)
 Call ID: 8afdaf9d-2b1a-4b2f-96cb-76fb36a1fa29
  Args:
    type: :Woman
    source: Isabelle_dOrleans
  AssignClass (8f2ae361-cd72-4cff-8b0e-1f9c4bc8000f)
 Call ID: 8f2ae361-cd72-4cff-8b0e-1f9c4bc8000f
  Args:
    type: :Person
    source: Isabelle_dOrleans
  AddTriple (eb9f0001-cde7-41e0-9d56-3af0b7ffcb5d)
 Call ID: eb9f0001-cde7-41e0-9d56-3af0b7ffcb5d
  Args:
    relation: :hasFather
    target: Michel_dOrleans
    source: Isabelle_dOrleans
  AddTriple (19d5af02-65fe-480f-8e72-ed0649671671)
 Call ID: 19d5af02-65fe-480f-8e72-ed0649671671
  Args:
    target: Beatrice_Pasquier_de_Franclieu
    relation: :hasMother
    source: Isabelle_dOrleans
  AddLiteral (0ca35812-84f1-4434-b801-f0076e1f295e)
 Call ID: 0ca35812-84f1-4434-b801-f0076e1f295e
  Args:
    literal_type: xsd:integer
    literal_value: 2012
    relation: :hasBirthYear
    source: Isabelle_dOrleans
  AssignClass (35558078-a3e3-4625-916e-9cc4441b88bb)
 Call ID: 35558078-a3e3-4625-916e-9cc4441b88bb
  Args:
    source: Elisabeth_Victoire_Jeanne_Marie_dOrleans
    type: :Woman
  AssignClass (1eea9cd4-aad8-4f7c-b050-2c316e40eb15)
 Call ID: 1eea9cd4-aad8-4f7c-b050-2c316e40eb15
  Args:
    source: Elisabeth_Victoire_Jeanne_Marie_dOrleans
    type: :Person
  AddTriple (ecbe175e-5a17-43b1-83dd-91f22e5b0c8d)
 Call ID: ecbe175e-5a17-43b1-83dd-91f22e5b0c8d
  Args:
    relation: :hasFather
    target: Charles_Philippe_Marie_Louis_dOrleans
    source: Elisabeth_Victoire_Jeanne_Marie_dOrleans
  AssignClass (c3150055-d1f5-4e6b-bad1-9911261fddd3)
 Call ID: c3150055-d1f5-4e6b-bad1-9911261fddd3
  Args:
    source: Naomi_Valeska
    type: :Woman
  AssignClass (0b66e34e-4799-41a8-80b7-c1983e40c3fa)
 Call ID: 0b66e34e-4799-41a8-80b7-c1983e40c3fa
  Args:
    source: Naomi_Valeska
    type: :Person
  AddTriple (90fa9ac5-33a3-4285-b776-503428aa2c18)
 Call ID: 90fa9ac5-33a3-4285-b776-503428aa2c18
  Args:
    relation: :hasMother
    target: Naomi_Valeska
    source: Elisabeth_Victoire_Jeanne_Marie_dOrleans
  AddLiteral (d6e17b93-6c93-4600-860b-aead0dda1815)
 Call ID: d6e17b93-6c93-4600-860b-aead0dda1815
  Args:
    source: Elisabeth_Victoire_Jeanne_Marie_dOrleans
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 2026
  Finish (8b8224c1-a61d-415c-9755-18e222b51f17)
 Call ID: 8b8224c1-a61d-415c-9755-18e222b51f17
  Args: