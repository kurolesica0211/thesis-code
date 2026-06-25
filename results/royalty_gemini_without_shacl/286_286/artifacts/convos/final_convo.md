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
Rafael of Orléans-Braganza (Portuguese: Rafael de Orléans e Bragança; born 24 April 1986) is a member of the Imperial House of Brazil.
He is the heir presumptive to his childless uncle, Prince Bertrand, the current head of the Vassouras branch of the House of Orléans-Braganza and one of the claimants to the defunct Brazilian Throne.
Rafael became heir presumptive following the death of his father, Prince Antônio, in November 2024.
Family

Born in Petrópolis, Brazil on 26 April 1986, he is the third child and second son of Prince Antônio de Orleans e Bragança and Princess Christine of Ligne.
He has an older brother and sister, Prince Pedro Luiz and Princess Amélia and a younger sister, Princess Maria Gabriela.
His name in full is Rafael Antonio Maria José Francisco Miguel Gabriel Gonzaga de Orléans e Bragança e Ligne.
His paternal grandparents were Prince Pedro Henrique of Orléans-Bragança, one of two claimants to be head of the Brazilian Imperial House, and Princess Maria Elisabeth of Bavaria.
His maternal grandparents were Antoine, 13th Prince of Ligne, and Princess Alix of Luxembourg.
His mother's family, the House of Ligne, is one of the oldest and most prominent Wallonian noble families still extant in Belgium.
Christine is a niece of Grand Duke Jean, who reigned in Luxembourg until his abdication in 2000.
Personal life

Rafael has a degree in manufacturing engineering from Pontifical Catholic University of Rio de Janeiro, working at the InBev subsidiary in London.
Rafael also has a partnership and a tourism enterprise with headquarters in New York, Paris and Rio de Janeiro.
Rafael has expressed in statements his desire to marry a princess who is part of "Catholic royalty or high nobility".
Appointments

In February 2022, after the floods that devastated the city of Petrópolis, Rafael came to the aid of the victims, bringing them essential goods that the imperial house received from monarchist supporters.
Honors

Genealogy

Ancestry

Patrilineal descent

Rafael is a member of the House of Orléans-Braganza, a sub-branch of the House of Bourbon, itself a branch of the House of Capet and of the Robertians.
Rafael's patriline is the line from which he is descended father to son.
It follows the Dukes of Orléans, the Kings of France, the Dukes and Counts of Vendôme, the Counts of La Marche, the first Duke of Bourbon, a Count of Clermont, and before them, again the Kings of France.



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
  AssignClass (da7de4f3-c333-4894-9dac-f7cc9e724702)
 Call ID: da7de4f3-c333-4894-9dac-f7cc9e724702
  Args:
    type: :Man
    source: Rafael_of_Orléans-Braganza
  AssignClass (78fb32d8-fb28-46e2-9b24-928eb2dc531c)
 Call ID: 78fb32d8-fb28-46e2-9b24-928eb2dc531c
  Args:
    type: :Person
    source: Rafael_of_Orléans-Braganza
  AddLiteral (8873296d-d9b0-4c87-9e49-45c8d64e933b)
 Call ID: 8873296d-d9b0-4c87-9e49-45c8d64e933b
  Args:
    source: Rafael_of_Orléans-Braganza
    literal_value: 1986
    relation: :hasBirthYear
    literal_type: xsd:integer
  AssignClass (03c33705-a441-4f55-9c29-bbec16de510d)
 Call ID: 03c33705-a441-4f55-9c29-bbec16de510d
  Args:
    type: :Man
    source: Prince_Bertrand
  AssignClass (62c739b5-7c22-47c3-918b-4a377fb15752)
 Call ID: 62c739b5-7c22-47c3-918b-4a377fb15752
  Args:
    source: Prince_Bertrand
    type: :Person
  AssignClass (83e4d9b3-c489-4d76-9239-3b685a9353b6)
 Call ID: 83e4d9b3-c489-4d76-9239-3b685a9353b6
  Args:
    type: :Man
    source: Prince_Antônio
  AssignClass (f79db54b-ddf4-4b27-bb2c-dfca2318f542)
 Call ID: f79db54b-ddf4-4b27-bb2c-dfca2318f542
  Args:
    source: Prince_Antônio
    type: :Person
  AddLiteral (a56e1b20-c913-40bf-9802-43b0f3863cc2)
 Call ID: a56e1b20-c913-40bf-9802-43b0f3863cc2
  Args:
    literal_type: xsd:integer
    literal_value: 2024
    relation: :hasDeathYear
    source: Prince_Antônio
  AssignClass (b771b978-fb37-4461-ba84-50d12200d7bb)
 Call ID: b771b978-fb37-4461-ba84-50d12200d7bb
  Args:
    type: :Woman
    source: Princess_Christine_of_Ligne
  AssignClass (66dc8d06-ce16-4716-a363-72b7c204f519)
 Call ID: 66dc8d06-ce16-4716-a363-72b7c204f519
  Args:
    type: :Person
    source: Princess_Christine_of_Ligne
  AddTriple (aa9bf5ba-f5f5-4edc-bec9-40bae458f023)
 Call ID: aa9bf5ba-f5f5-4edc-bec9-40bae458f023
  Args:
    target: Prince_Antônio
    relation: :hasFather
    source: Rafael_of_Orléans-Braganza
  AddTriple (19e88222-f1af-4cfa-a6a6-7e661d110f55)
 Call ID: 19e88222-f1af-4cfa-a6a6-7e661d110f55
  Args:
    target: Princess_Christine_of_Ligne
    source: Rafael_of_Orléans-Braganza
    relation: :hasMother
  AssignClass (9347a080-fcbc-4947-b9e4-aa83d963d6c2)
 Call ID: 9347a080-fcbc-4947-b9e4-aa83d963d6c2
  Args:
    type: :Man
    source: Prince_Pedro_Luiz
  AssignClass (55385006-818c-4867-8c73-0407b9ca00c0)
 Call ID: 55385006-818c-4867-8c73-0407b9ca00c0
  Args:
    type: :Person
    source: Prince_Pedro_Luiz
  AddTriple (646f1be4-e792-464f-8417-49632d7e8f5b)
 Call ID: 646f1be4-e792-464f-8417-49632d7e8f5b
  Args:
    target: Prince_Pedro_Luiz
    relation: :hasBrother
    source: Rafael_of_Orléans-Braganza
  AssignClass (21a14ef2-4940-4119-a6be-8b18be67d3d5)
 Call ID: 21a14ef2-4940-4119-a6be-8b18be67d3d5
  Args:
    source: Princess_Amélia
    type: :Woman
  AssignClass (d8ccc430-09d6-4c68-bf53-f5518fc20812)
 Call ID: d8ccc430-09d6-4c68-bf53-f5518fc20812
  Args:
    source: Princess_Amélia
    type: :Person
  AddTriple (4cb9046d-48fe-433f-b4f9-ca581464ee85)
 Call ID: 4cb9046d-48fe-433f-b4f9-ca581464ee85
  Args:
    source: Rafael_of_Orléans-Braganza
    relation: :hasSister
    target: Princess_Amélia
  AssignClass (61afbaf1-9ef1-460d-845a-a0ef74b9864a)
 Call ID: 61afbaf1-9ef1-460d-845a-a0ef74b9864a
  Args:
    type: :Woman
    source: Princess_Maria_Gabriela
  AssignClass (65834b3f-ca46-4301-b4d1-3727dac85074)
 Call ID: 65834b3f-ca46-4301-b4d1-3727dac85074
  Args:
    source: Princess_Maria_Gabriela
    type: :Person
  AddTriple (bcc4b2eb-14f9-4dd4-ac46-262ae2ca231f)
 Call ID: bcc4b2eb-14f9-4dd4-ac46-262ae2ca231f
  Args:
    relation: :hasSister
    source: Rafael_of_Orléans-Braganza
    target: Princess_Maria_Gabriela
  AssignClass (dbaa1cd3-bd0a-41a4-aa70-560ac4553d48)
 Call ID: dbaa1cd3-bd0a-41a4-aa70-560ac4553d48
  Args:
    type: :Man
    source: Prince_Pedro_Henrique
  AssignClass (b46d8d28-2619-4bc2-a376-aff45bc73588)
 Call ID: b46d8d28-2619-4bc2-a376-aff45bc73588
  Args:
    source: Prince_Pedro_Henrique
    type: :Person
  AssignClass (fc704d2b-4297-4148-9e9e-463e4f74bda2)
 Call ID: fc704d2b-4297-4148-9e9e-463e4f74bda2
  Args:
    type: :Woman
    source: Princess_Maria_Elisabeth_of_Bavaria
  AssignClass (5f377d21-deca-478a-9d45-9be65d364ed3)
 Call ID: 5f377d21-deca-478a-9d45-9be65d364ed3
  Args:
    source: Princess_Maria_Elisabeth_of_Bavaria
    type: :Person
  AssignClass (25cefc79-b1dd-4f48-92e5-80484c42537e)
 Call ID: 25cefc79-b1dd-4f48-92e5-80484c42537e
  Args:
    source: Antoine_13th_Prince_of_Ligne
    type: :Man
  AssignClass (222dcfd5-8228-4cea-9593-b01f2030f548)
 Call ID: 222dcfd5-8228-4cea-9593-b01f2030f548
  Args:
    source: Antoine_13th_Prince_of_Ligne
    type: :Person
  AssignClass (4880d867-8529-4687-9998-b5301cc20fe7)
 Call ID: 4880d867-8529-4687-9998-b5301cc20fe7
  Args:
    type: :Woman
    source: Princess_Alix_of_Luxembourg
  AssignClass (15181654-e29c-414c-99e4-a31c67422455)
 Call ID: 15181654-e29c-414c-99e4-a31c67422455
  Args:
    source: Princess_Alix_of_Luxembourg
    type: :Person
  AddTriple (dbab2462-6d2d-427a-8998-262c6d8e3235)
 Call ID: dbab2462-6d2d-427a-8998-262c6d8e3235
  Args:
    target: Prince_Pedro_Henrique
    relation: :hasFather
    source: Prince_Antônio
  AddTriple (893b7b5e-5ea5-4061-a1cb-62bd43dc0268)
 Call ID: 893b7b5e-5ea5-4061-a1cb-62bd43dc0268
  Args:
    target: Princess_Maria_Elisabeth_of_Bavaria
    relation: :hasMother
    source: Prince_Antônio
  AddTriple (f45c4b71-cb6f-4182-b975-61eadd0afaa3)
 Call ID: f45c4b71-cb6f-4182-b975-61eadd0afaa3
  Args:
    target: Antoine_13th_Prince_of_Ligne
    source: Princess_Christine_of_Ligne
    relation: :hasFather
  AddTriple (1cc842e2-c3c0-4460-ac8f-87ea7924e63c)
 Call ID: 1cc842e2-c3c0-4460-ac8f-87ea7924e63c
  Args:
    target: Princess_Alix_of_Luxembourg
    relation: :hasMother
    source: Princess_Christine_of_Ligne
  Finish (a43a0ed6-8427-4a60-a5db-79884920054c)
 Call ID: a43a0ed6-8427-4a60-a5db-79884920054c
  Args: