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
Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Hugo de Bourbon de Parme (Carlos Hugo Roderik Sybren; born 20 January 1997), formerly Hugo Klynstra, is a member of the extended Dutch royal family as the son of Prince Carlos, Hereditary Duke of Parma.
He was the first great-grandchild of Queen Juliana of the Netherlands.
Born out of wedlock, he was denied titles and family rights by his father until the Dutch Council of State ruled in his favor in 2018, granting him the style and title of His Royal Highness Prince Carlos Hugo
Roderik Sybren de Bourbon de Parme.
Despite the ruling, he is neither a member of the Dutch royal house (although considered a member of the extended Dutch royal family) nor a member of the House of Bourbon-Parma and is not in the line of succession to the defunct Parmese throne.
Early life and family

Carlos Hugo Roderik Sybren Klynstra was born in Nijmegen on 20 January 1997 to Prince Carlos de Bourbon de Parme, Prince of Piacenza and his friend Brigitte Klynstra.
Due to being an illegitimate son, he was not born a prince.
His father told Dutch media that Hugo's birth was "his mother's wish" and an "independent decision", denying his son any family rights.
His maternal grandmother, Ingrid Pieksma-Klynstra, was the wife of Adolph Roderik Ernst Leopold, Count of Rechteren-Limpurg.
Through his father, he is a grandson of Carlos Hugo, Duke of Parma and Princess Irene of the Netherlands.
He is the first great-grandchild of Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
He is also a great-grandson of Prince Xavier of Bourbon-Parma and Madeleine de Bourbon-Busset.
Upon the death of his grandfather, Carlos Hugo, in 2010, his father became the titular Duke of Parma and Piacenza, Carlist claimant to the Spanish throne, and the Head of the House of Bourbon-Parma.
According to a royal decree of Queen Beatrix in 1996, his father is also a Dutch prince.
He is the half-brother of Princess Luisa of Parma, Marchioness of Castell'Arquato, Princess Cecilia of Parma, Countess of Berceto and Prince Carlos of Parma, The Prince of Piacenza.
Legal dispute over title

Upon turning eighteen in 2015, Hugo went to court to have his surname changed from Klynstra to his father's surname, 'de Bourbon de Parme', and claimed the dutch noble title of prince.
The Hereditary Duke of Parma insisted that he had a formal agreement with Hugo's mother that their relationship was "no-strings-attached" and that there would be "no family entanglement" following Hugo's conception.
In 2016 the Ministry of Justice and Security ruled in favor of Hugo's claim and granted him the use of his father's surname.
On 28 February 2018, the Dutch Council of State ruled in Hugo's favor, stating that Dutch law on nobility was clear and that the circumstances of Hugo's birth are irrelevant, granting Hugo the right to claim both his father's surname and (dutch) noble title and address.
As such, he became His Royal Highness Prince Carlos Hugo Roderik Sybren de Bourbon de Parme.
The title of 'Prince(ss) de Bourbon de Parme' is a Dutch title, bestowed by Queen Beatrix in 1996, and does not mean that Hugo automatically became a member of the House of Bourbon-Parma.
The court ruling stated that membership to the House of Bourbon-Parma is "a private matter for the royal house itself".
As such, he is not in the line of succession to the defunct Parma throne.
Titles and styles

References




2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (48adfac6-aa79-4284-9e68-bb882037af37)
 Call ID: 48adfac6-aa79-4284-9e68-bb882037af37
  Args:
    type: :Man
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  AssignClass (ac7ffbe6-7fe3-41c8-8f25-9d232305b09c)
 Call ID: ac7ffbe6-7fe3-41c8-8f25-9d232305b09c
  Args:
    type: :Person
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  AddLiteral (c4bade6a-4b5b-4c07-ba97-ef5b5f44bd85)
 Call ID: c4bade6a-4b5b-4c07-ba97-ef5b5f44bd85
  Args:
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
    literal_type: xsd:string
    literal_value: Carlos Hugo Roderik Sybren Klynstra
    relation: :formerlyKnownAs
  AddLiteral (09b8f4d0-4dc5-4df6-94d1-3df158ed96e4)
 Call ID: 09b8f4d0-4dc5-4df6-94d1-3df158ed96e4
  Args:
    literal_value: 1997
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
  AssignClass (8dc0a55f-7f41-46cc-8bbb-8e8c06321759)
 Call ID: 8dc0a55f-7f41-46cc-8bbb-8e8c06321759
  Args:
    type: :Man
    source: Prince_Carlos_de_Bourbon_de_Parme
  AssignClass (e0da910d-2b1f-4005-a13e-0d3ab29e792f)
 Call ID: e0da910d-2b1f-4005-a13e-0d3ab29e792f
  Args:
    type: :Person
    source: Prince_Carlos_de_Bourbon_de_Parme
  AssignClass (7336c8a8-2b3a-461a-b9d8-104cc1c829fd)
 Call ID: 7336c8a8-2b3a-461a-b9d8-104cc1c829fd
  Args:
    type: :Woman
    source: Brigitte_Klynstra
  AssignClass (4d7b8750-5f55-45ec-96ed-3eabe0e53e5d)
 Call ID: 4d7b8750-5f55-45ec-96ed-3eabe0e53e5d
  Args:
    type: :Person
    source: Brigitte_Klynstra
  AddTriple (bc628804-a492-48ef-bf11-43e1b7d7e235)
 Call ID: bc628804-a492-48ef-bf11-43e1b7d7e235
  Args:
    target: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
    source: Prince_Carlos_de_Bourbon_de_Parme
    relation: :isFatherOf
  AddTriple (507eda0e-6fe7-4e6b-b6f7-3207a96d7827)
 Call ID: 507eda0e-6fe7-4e6b-b6f7-3207a96d7827
  Args:
    source: Brigitte_Klynstra
    target: Prince_Carlos_Hugo_Roderik_Sybren_de_Bourbon_de_Parme
    relation: :isMotherOf
  AssignClass (86b34512-ee1d-4037-a965-cb46d37c055d)
 Call ID: 86b34512-ee1d-4037-a965-cb46d37c055d
  Args:
    type: :Woman
    source: Ingrid_Pieksma-Klynstra
  AssignClass (5a11fd9a-1042-48e9-9139-91ad35106d63)
 Call ID: 5a11fd9a-1042-48e9-9139-91ad35106d63
  Args:
    type: :Person
    source: Ingrid_Pieksma-Klynstra
  AddTriple (71432253-51b1-4973-9718-4aee54788cfe)
 Call ID: 71432253-51b1-4973-9718-4aee54788cfe
  Args:
    relation: :isMotherOf
    source: Ingrid_Pieksma-Klynstra
    target: Brigitte_Klynstra
  AssignClass (6d25d42b-6e14-40dd-ae99-0f431b4e878f)
 Call ID: 6d25d42b-6e14-40dd-ae99-0f431b4e878f
  Args:
    type: :Man
    source: Adolph_Roderik_Ernst_Leopold_Count_of_Rechteren-Limpurg
  AssignClass (fb434885-bd8f-4abd-b0e7-c018829a347f)
 Call ID: fb434885-bd8f-4abd-b0e7-c018829a347f
  Args:
    type: :Person
    source: Adolph_Roderik_Ernst_Leopold_Count_of_Rechteren-Limpurg
  AddTriple (6117d1e5-0539-4c4b-bd6c-8a779b256af0)
 Call ID: 6117d1e5-0539-4c4b-bd6c-8a779b256af0
  Args:
    target: Brigitte_Klynstra
    source: Adolph_Roderik_Ernst_Leopold_Count_of_Rechteren-Limpurg
    relation: :isFatherOf
  AssignClass (ef0f8628-168a-44d3-bf6b-e27baf62f7ba)
 Call ID: ef0f8628-168a-44d3-bf6b-e27baf62f7ba
  Args:
    type: :Man
    source: Carlos_Hugo_Duke_of_Parma
  AssignClass (9dfe776e-c001-4a17-8604-dd1a05bef872)
 Call ID: 9dfe776e-c001-4a17-8604-dd1a05bef872
  Args:
    type: :Person
    source: Carlos_Hugo_Duke_of_Parma
  AssignClass (a48ba877-0c62-4a48-9f04-59ead1a1955f)
 Call ID: a48ba877-0c62-4a48-9f04-59ead1a1955f
  Args:
    type: :Woman
    source: Princess_Irene_of_the_Netherlands
  AssignClass (14e12472-0073-4877-9875-9217ff50b3ef)
 Call ID: 14e12472-0073-4877-9875-9217ff50b3ef
  Args:
    type: :Person
    source: Princess_Irene_of_the_Netherlands
  AddTriple (521e4283-74e5-40d0-a1e0-e65a007123d0)
 Call ID: 521e4283-74e5-40d0-a1e0-e65a007123d0
  Args:
    relation: :isFatherOf
    source: Carlos_Hugo_Duke_of_Parma
    target: Prince_Carlos_de_Bourbon_de_Parme
  AddTriple (1bd7c3a8-3563-4f95-a20c-f5255d605757)
 Call ID: 1bd7c3a8-3563-4f95-a20c-f5255d605757
  Args:
    relation: :isMotherOf
    target: Prince_Carlos_de_Bourbon_de_Parme
    source: Princess_Irene_of_the_Netherlands
  AssignClass (525fcc6a-5312-4e26-95b8-ef02e3374430)
 Call ID: 525fcc6a-5312-4e26-95b8-ef02e3374430
  Args:
    type: :Woman
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (79d18ae6-9b66-462e-b702-9f0bdb983a07)
 Call ID: 79d18ae6-9b66-462e-b702-9f0bdb983a07
  Args:
    type: :Person
    source: Queen_Juliana_of_the_Netherlands
  AssignClass (5d97b768-7638-47f8-8f2b-9a1a5e973dc6)
 Call ID: 5d97b768-7638-47f8-8f2b-9a1a5e973dc6
  Args:
    type: :Man
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (2cd63035-e4eb-4492-87ef-483ad83b53a3)
 Call ID: 2cd63035-e4eb-4492-87ef-483ad83b53a3
  Args:
    type: :Person
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AddTriple (26422b2f-315f-44e7-9d6b-d6589c90d099)
 Call ID: 26422b2f-315f-44e7-9d6b-d6589c90d099
  Args:
    target: Princess_Irene_of_the_Netherlands
    source: Queen_Juliana_of_the_Netherlands
    relation: :isMotherOf
  AddTriple (5528e7ec-d331-4ae4-84bf-9753651caf8e)
 Call ID: 5528e7ec-d331-4ae4-84bf-9753651caf8e
  Args:
    relation: :isFatherOf
    target: Princess_Irene_of_the_Netherlands
    source: Prince_Bernhard_of_Lippe-Biesterfeld
  AssignClass (95174af8-4dc7-4cfc-affd-51ea694badba)
 Call ID: 95174af8-4dc7-4cfc-affd-51ea694badba
  Args:
    type: :Man
    source: Prince_Xavier_of_Bourbon-Parma
  AssignClass (4a74ef66-4729-468d-92d2-f5f51032a882)
 Call ID: 4a74ef66-4729-468d-92d2-f5f51032a882
  Args:
    type: :Person
    source: Prince_Xavier_of_Bourbon-Parma
  AssignClass (45e8189f-794e-42b0-9e65-b5e5609f7c8f)
 Call ID: 45e8189f-794e-42b0-9e65-b5e5609f7c8f
  Args:
    type: :Woman
    source: Madeleine_de_Bourbon-Busset
  AssignClass (d8401bdf-fd06-47da-b5b0-75c36df6b9d8)
 Call ID: d8401bdf-fd06-47da-b5b0-75c36df6b9d8
  Args:
    type: :Person
    source: Madeleine_de_Bourbon-Busset
  AddTriple (cb0afeff-fec3-40e2-8b4f-4fde9988a5a7)
 Call ID: cb0afeff-fec3-40e2-8b4f-4fde9988a5a7
  Args:
    target: Carlos_Hugo_Duke_of_Parma
    source: Prince_Xavier_of_Bourbon-Parma
    relation: :isFatherOf
  AddTriple (2dedaece-b649-4a43-8218-2710d5e02fe0)
 Call ID: 2dedaece-b649-4a43-8218-2710d5e02fe0
  Args:
    relation: :isMotherOf
    source: Madeleine_de_Bourbon-Busset
    target: Carlos_Hugo_Duke_of_Parma
  AssignClass (d2fcf32b-e2cb-45dd-abc9-7e07783d0601)
 Call ID: d2fcf32b-e2cb-45dd-abc9-7e07783d0601
  Args:
    type: :Woman
    source: Princess_Luisa_of_Parma
  AssignClass (4188980d-c117-4386-87fa-071ba0006bf3)
 Call ID: 4188980d-c117-4386-87fa-071ba0006bf3
  Args:
    type: :Person
    source: Princess_Luisa_of_Parma
  AssignClass (6635f4ca-9266-482b-9f58-5ffe9a81448a)
 Call ID: 6635f4ca-9266-482b-9f58-5ffe9a81448a
  Args:
    type: :Woman
    source: Princess_Cecilia_of_Parma
  AssignClass (0b742ca1-27ad-46b3-961b-394eb9138a3c)
 Call ID: 0b742ca1-27ad-46b3-961b-394eb9138a3c
  Args:
    type: :Person
    source: Princess_Cecilia_of_Parma
  AssignClass (6952b057-8a39-4628-bf77-50e365b744da)
 Call ID: 6952b057-8a39-4628-bf77-50e365b744da
  Args:
    type: :Man
    source: Prince_Carlos_of_Parma
  AssignClass (a904a9a6-d55b-4c40-877b-1767248084b8)
 Call ID: a904a9a6-d55b-4c40-877b-1767248084b8
  Args:
    type: :Person
    source: Prince_Carlos_of_Parma
  AddTriple (de672ee4-3c15-40e7-8ac3-0a1f38f27d33)
 Call ID: de672ee4-3c15-40e7-8ac3-0a1f38f27d33
  Args:
    relation: :isFatherOf
    source: Prince_Carlos_de_Bourbon_de_Parme
    target: Princess_Luisa_of_Parma
  AddTriple (6f84526d-8253-4c43-8ffe-2ec0f3d2372b)
 Call ID: 6f84526d-8253-4c43-8ffe-2ec0f3d2372b
  Args:
    source: Prince_Carlos_de_Bourbon_de_Parme
    target: Princess_Cecilia_of_Parma
    relation: :isFatherOf
  AddTriple (348ea6ea-527e-41fc-92e4-9304291f7b55)
 Call ID: 348ea6ea-527e-41fc-92e4-9304291f7b55
  Args:
    relation: :isFatherOf
    source: Prince_Carlos_de_Bourbon_de_Parme
    target: Prince_Carlos_of_Parma
  Finish (d73c0b74-dcd5-4f25-9a0b-1514f409ef9b)
 Call ID: d73c0b74-dcd5-4f25-9a0b-1514f409ef9b
  Args: