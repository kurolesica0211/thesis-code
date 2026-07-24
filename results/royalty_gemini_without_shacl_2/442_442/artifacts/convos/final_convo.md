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
  AssignClass (170a6e11-0c7f-4b15-b28d-22b150cffca8)
 Call ID: 170a6e11-0c7f-4b15-b28d-22b150cffca8
  Args:
    source: CarlosHugoRoderikSybrenDeBourbonDeParme
    type: :Man
  AssignClass (00ebd755-6b43-4218-b69f-e7f09018a3e2)
 Call ID: 00ebd755-6b43-4218-b69f-e7f09018a3e2
  Args:
    type: :Person
    source: CarlosHugoRoderikSybrenDeBourbonDeParme
  AddLiteral (a58e399e-6cb4-4ee8-933f-ca408706769c)
 Call ID: a58e399e-6cb4-4ee8-933f-ca408706769c
  Args:
    source: CarlosHugoRoderikSybrenDeBourbonDeParme
    literal_value: 1997
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (1ce80a48-41d6-4888-9d48-c5773b966713)
 Call ID: 1ce80a48-41d6-4888-9d48-c5773b966713
  Args:
    source: CarlosHugoRoderikSybrenDeBourbonDeParme
    literal_value: Hugo Klynstra
    relation: :formerlyKnownAs
    literal_type: xsd:string
  AssignClass (8a4d1f94-46ae-4674-8f8d-e43d78033c25)
 Call ID: 8a4d1f94-46ae-4674-8f8d-e43d78033c25
  Args:
    type: :Man
    source: PrinceCarlosDeBourbonDeParme
  AssignClass (8be7c744-626b-4425-8d7e-f47c9abb64a4)
 Call ID: 8be7c744-626b-4425-8d7e-f47c9abb64a4
  Args:
    source: PrinceCarlosDeBourbonDeParme
    type: :Person
  AssignClass (4452337c-ee9d-44db-bc94-d6ac0a1c6b84)
 Call ID: 4452337c-ee9d-44db-bc94-d6ac0a1c6b84
  Args:
    source: BrigitteKlynstra
    type: :Woman
  AssignClass (6f621a18-4d29-4716-8c1b-d04498385cd1)
 Call ID: 6f621a18-4d29-4716-8c1b-d04498385cd1
  Args:
    source: BrigitteKlynstra
    type: :Person
  AddTriple (9d8dfc17-15eb-489d-a7c1-2fe6c6280a14)
 Call ID: 9d8dfc17-15eb-489d-a7c1-2fe6c6280a14
  Args:
    target: PrinceCarlosDeBourbonDeParme
    source: CarlosHugoRoderikSybrenDeBourbonDeParme
    relation: :hasFather
  AddTriple (c0bf0805-f3e0-4b58-b1d6-0079b8331691)
 Call ID: c0bf0805-f3e0-4b58-b1d6-0079b8331691
  Args:
    target: BrigitteKlynstra
    relation: :hasMother
    source: CarlosHugoRoderikSybrenDeBourbonDeParme
  AssignClass (1b801317-255d-4c5d-9825-a7e2912bdc4c)
 Call ID: 1b801317-255d-4c5d-9825-a7e2912bdc4c
  Args:
    type: :Woman
    source: IngridPieksmaKlynstra
  AssignClass (5dc9aa72-a341-4444-8767-dd9068b67b03)
 Call ID: 5dc9aa72-a341-4444-8767-dd9068b67b03
  Args:
    type: :Person
    source: IngridPieksmaKlynstra
  AddTriple (f1cb293f-4369-441e-9198-c6bd791b3b7d)
 Call ID: f1cb293f-4369-441e-9198-c6bd791b3b7d
  Args:
    target: IngridPieksmaKlynstra
    source: BrigitteKlynstra
    relation: :hasMother
  AssignClass (a3716110-a122-4d47-ac8c-6f9d38aac2bf)
 Call ID: a3716110-a122-4d47-ac8c-6f9d38aac2bf
  Args:
    type: :Man
    source: AdolphRoderikErnstLeopold
  AssignClass (5ec56ce3-8b9b-4350-9cbb-5a165df4c935)
 Call ID: 5ec56ce3-8b9b-4350-9cbb-5a165df4c935
  Args:
    type: :Person
    source: AdolphRoderikErnstLeopold
  AddTriple (966a3240-00ba-486b-b83e-a37e1c09656a)
 Call ID: 966a3240-00ba-486b-b83e-a37e1c09656a
  Args:
    relation: :hasFather
    source: BrigitteKlynstra
    target: AdolphRoderikErnstLeopold
  AssignClass (a36f6911-2e5b-4cb9-8239-5d6d2c0df85d)
 Call ID: a36f6911-2e5b-4cb9-8239-5d6d2c0df85d
  Args:
    source: CarlosHugoDukeOfParma
    type: :Man
  AssignClass (c776b2b1-07b8-44c5-8f56-7f8540608802)
 Call ID: c776b2b1-07b8-44c5-8f56-7f8540608802
  Args:
    type: :Person
    source: CarlosHugoDukeOfParma
  AssignClass (9f2ec36b-1f28-4b5f-980f-8aca91318845)
 Call ID: 9f2ec36b-1f28-4b5f-980f-8aca91318845
  Args:
    type: :Woman
    source: PrincessIreneOfTheNetherlands
  AssignClass (fb76f57c-c703-40b6-a42b-5e676222c13f)
 Call ID: fb76f57c-c703-40b6-a42b-5e676222c13f
  Args:
    type: :Person
    source: PrincessIreneOfTheNetherlands
  AddTriple (16c53340-d97e-402d-ba33-200b601c0ac3)
 Call ID: 16c53340-d97e-402d-ba33-200b601c0ac3
  Args:
    relation: :hasFather
    source: PrinceCarlosDeBourbonDeParme
    target: CarlosHugoDukeOfParma
  AddTriple (d6aaecdc-0ed1-4b84-80b3-20e92795d5ab)
 Call ID: d6aaecdc-0ed1-4b84-80b3-20e92795d5ab
  Args:
    relation: :hasMother
    source: PrinceCarlosDeBourbonDeParme
    target: PrincessIreneOfTheNetherlands
  AssignClass (c1b14da2-fa1c-438a-acbc-737b18425976)
 Call ID: c1b14da2-fa1c-438a-acbc-737b18425976
  Args:
    type: :Woman
    source: QueenJulianaOfTheNetherlands
  AssignClass (f2195923-3aa6-46b5-9723-cada8863442e)
 Call ID: f2195923-3aa6-46b5-9723-cada8863442e
  Args:
    source: QueenJulianaOfTheNetherlands
    type: :Person
  AssignClass (e94a603f-f3cc-4bd7-bb76-6d65a97f7601)
 Call ID: e94a603f-f3cc-4bd7-bb76-6d65a97f7601
  Args:
    source: PrinceBernhardOfLippeBiesterfeld
    type: :Man
  AssignClass (260076be-1fee-4832-a802-c68d1dee7d44)
 Call ID: 260076be-1fee-4832-a802-c68d1dee7d44
  Args:
    source: PrinceBernhardOfLippeBiesterfeld
    type: :Person
  AssignClass (b209eac2-500f-453c-b1c2-05e9932662b1)
 Call ID: b209eac2-500f-453c-b1c2-05e9932662b1
  Args:
    type: :Man
    source: PrinceXavierOfBourbonParma
  AssignClass (b1a6f315-e7fe-4984-92dc-edc66f330753)
 Call ID: b1a6f315-e7fe-4984-92dc-edc66f330753
  Args:
    source: PrinceXavierOfBourbonParma
    type: :Person
  AssignClass (6830f538-615b-4500-836e-80a058849a82)
 Call ID: 6830f538-615b-4500-836e-80a058849a82
  Args:
    type: :Woman
    source: MadeleineDeBourbonBusset
  AssignClass (a202c331-8331-4b3a-bfee-4feb62392512)
 Call ID: a202c331-8331-4b3a-bfee-4feb62392512
  Args:
    type: :Person
    source: MadeleineDeBourbonBusset
  AssignClass (cd4ff7a5-0106-4e4c-b923-0da3be7cc919)
 Call ID: cd4ff7a5-0106-4e4c-b923-0da3be7cc919
  Args:
    type: :Woman
    source: PrincessLuisaOfParma
  AssignClass (ee36f7f5-98e9-49c6-954d-ea725ecb48a4)
 Call ID: ee36f7f5-98e9-49c6-954d-ea725ecb48a4
  Args:
    type: :Person
    source: PrincessLuisaOfParma
  AssignClass (3f6be49e-3702-4817-b7ce-52a3825a5316)
 Call ID: 3f6be49e-3702-4817-b7ce-52a3825a5316
  Args:
    type: :Woman
    source: PrincessCeciliaOfParma
  AssignClass (2f1bee36-bcf2-42e6-8028-78a49f2c8b7b)
 Call ID: 2f1bee36-bcf2-42e6-8028-78a49f2c8b7b
  Args:
    type: :Person
    source: PrincessCeciliaOfParma
  AssignClass (d06b3556-dbb3-4670-ae28-dfe78373f02e)
 Call ID: d06b3556-dbb3-4670-ae28-dfe78373f02e
  Args:
    source: PrinceCarlosOfParma
    type: :Man
  AssignClass (5c34300e-272f-4fac-b956-8620430f2c4e)
 Call ID: 5c34300e-272f-4fac-b956-8620430f2c4e
  Args:
    source: PrinceCarlosOfParma
    type: :Person
  AddTriple (c89ea995-4925-402d-a128-f7c8c58fd7ca)
 Call ID: c89ea995-4925-402d-a128-f7c8c58fd7ca
  Args:
    relation: :hasFather
    source: PrincessLuisaOfParma
    target: PrinceCarlosDeBourbonDeParme
  AddTriple (1a7045b0-e432-4940-8d22-aa57addd23e6)
 Call ID: 1a7045b0-e432-4940-8d22-aa57addd23e6
  Args:
    target: PrinceCarlosDeBourbonDeParme
    relation: :hasFather
    source: PrincessCeciliaOfParma
  AddTriple (a367ade3-e627-483b-b5eb-6d012412eabd)
 Call ID: a367ade3-e627-483b-b5eb-6d012412eabd
  Args:
    target: PrinceCarlosDeBourbonDeParme
    relation: :hasFather
    source: PrinceCarlosOfParma
  Finish (debb0574-11d2-4565-bea9-d1b3f9150261)
 Call ID: debb0574-11d2-4565-bea9-d1b3f9150261
  Args: