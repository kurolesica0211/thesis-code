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
Princess Nuria


Princess Françoise


Princess Mariam


Princess Monique


Prince Juan Jorge de Bagration-Mukhrani (born 18 August 1977) is a Spanish-born Georgian prince and member of the House of Mukhrani of the Bagrationi dynasty and a distant relation to the Spanish royal family.
Early life and family

Prince Juan Jorge de Bagration-Mukhrani was born on 18 August 1977 in Madrid to Prince Bagrat de Bagration y de Baviera and Doña María del Carmen de Ulloa y Suelves.
His paternal grandfather, Prince Irakli Bagration of Mukhrani, was exiled from Georgia during the invasion of the Red Army, living in Germany, Italy, and finally settling in Spain.
His paternal grandmother, Infanta María de las Mercedes of Spain was a member of the Spanish royal family and the German House of Wittelsbach; she was the daughter of Prince Ferdinand of Bavaria, granddaughter of Alfonso XII of Spain, and niece of Alfonso XIII of Spain.
His maternal grandfather was Gonzalo Maria de Ulloa y Ramírez de Haro, Marqués de Castro-Serna, Count de Adanero.
Prince Juan's parents divorced in 2005 and his father remarried in 2009 to Françoise Cazaudehore.
Prince Juan is a member of the House of Mukhrani, a branch of the Bagrationi dynasty that ruled Georgia from the Middle Ages until the nineteenth century, when Georgia was annexed into the Russian Empire.
Prince Juan studied at Collège Alpin International Beau Soleil, a boarding school in Villars-sur-Ollon, Switzerland and was a schoolmate and childhood friend of Cayetano Rivera Ordóñez.
Personal life

Prince Juan met Kristine Dzidziguri, a Georgian model, in 2014.
They were married a few months later in a civil ceremony on 10 May 2014 in Ronda, Spain.
The couple began planning a religious ceremony but were delayed due to social and political conflicts within Georgia and because of Prince Juan's father's declining health.
On 2 June 2018, Prince Juan and Dzidziguri received a blessing from Ilia II of Georgia, the Catholicos-Patriarch of All Georgia.
Their wedding reception was held at the Palace of Mukhrani.
Later during their Indonesian tour, Prince Juan and Princess Kristine attended a gala lunch focused on establishing a cultural relationship between Indonesia and Georgia.
Prince Juan is the founder of the Georgian Foundation, a non-profit organization that promotes Georgian culture.
In October 2019 he launched a wine brand called Prince Ioane Bagrationi wines.



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
  AssignClass (205b7791-985d-4c23-9e3f-7ef4c3dd40f8)
 Call ID: 205b7791-985d-4c23-9e3f-7ef4c3dd40f8
  Args:
    type: :Woman
    source: Princess_Nuria
  AssignClass (4e78d06f-93cd-4494-aa03-4e8e26931446)
 Call ID: 4e78d06f-93cd-4494-aa03-4e8e26931446
  Args:
    type: :Woman
    source: Princess_Françoise
  AssignClass (b0b1ca5d-17f7-4c85-b7cf-c36f74d39484)
 Call ID: b0b1ca5d-17f7-4c85-b7cf-c36f74d39484
  Args:
    type: :Woman
    source: Princess_Mariam
  AssignClass (307b9c9f-5fbd-41a5-9f86-83255c25e9aa)
 Call ID: 307b9c9f-5fbd-41a5-9f86-83255c25e9aa
  Args:
    type: :Woman
    source: Princess_Monique
  AssignClass (fdbc648a-e7e0-4a25-a3ce-8729bc7935f2)
 Call ID: fdbc648a-e7e0-4a25-a3ce-8729bc7935f2
  Args:
    type: :Man
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AddLiteral (4cb534ca-8bc4-4a39-b754-8cfee42ea65d)
 Call ID: 4cb534ca-8bc4-4a39-b754-8cfee42ea65d
  Args:
    literal_value: 1977
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (4c08a02d-3dc2-46fb-857a-f70127c49772)
 Call ID: 4c08a02d-3dc2-46fb-857a-f70127c49772
  Args:
    type: :Man
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (d2554f50-0709-4094-82e3-d358c49b585d)
 Call ID: d2554f50-0709-4094-82e3-d358c49b585d
  Args:
    type: :Woman
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
  AddTriple (c5647d48-6bfc-4a6f-9d64-4e34fdc74a1f)
 Call ID: c5647d48-6bfc-4a6f-9d64-4e34fdc74a1f
  Args:
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
    relation: :hasFather
    target: Prince_Bagrat_de_Bagration_y_de_Baviera
  AddTriple (0a6ed133-7e57-48aa-b9ad-942e57ee7a20)
 Call ID: 0a6ed133-7e57-48aa-b9ad-942e57ee7a20
  Args:
    target: Doña_María_del_Carmen_de_Ulloa_y_Suelves
    relation: :hasMother
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (ff1d36a9-b0dd-41d6-b357-9253c894004f)
 Call ID: ff1d36a9-b0dd-41d6-b357-9253c894004f
  Args:
    type: :Man
    source: Prince_Irakli_Bagration_of_Mukhrani
  AddTriple (7cec990a-638b-4740-9895-2cc15c9423b4)
 Call ID: 7cec990a-638b-4740-9895-2cc15c9423b4
  Args:
    relation: :hasFather
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    target: Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (a085089f-ae23-40dd-b36d-596d6ca58389)
 Call ID: a085089f-ae23-40dd-b36d-596d6ca58389
  Args:
    type: :Woman
    source: Infanta_María_de_las_Mercedes_of_Spain
  AddTriple (d3991c25-6b65-44ea-bde0-69a4a879a8d4)
 Call ID: d3991c25-6b65-44ea-bde0-69a4a879a8d4
  Args:
    target: Infanta_María_de_las_Mercedes_of_Spain
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasMother
  AssignClass (d8a7f039-ba9a-44c7-821f-01e741cd42e7)
 Call ID: d8a7f039-ba9a-44c7-821f-01e741cd42e7
  Args:
    type: :Man
    source: Prince_Ferdinand_of_Bavaria
  AddTriple (a1e05070-5bb4-4764-8075-652323f1cbd5)
 Call ID: a1e05070-5bb4-4764-8075-652323f1cbd5
  Args:
    target: Prince_Ferdinand_of_Bavaria
    source: Infanta_María_de_las_Mercedes_of_Spain
    relation: :hasFather
  AssignClass (10d9642e-060f-426d-b70c-029537f3a1b4)
 Call ID: 10d9642e-060f-426d-b70c-029537f3a1b4
  Args:
    type: :Man
    source: Alfonso_XII_of_Spain
  AssignClass (d07f2d3b-38b1-49f2-bf06-ce7fbbb5b391)
 Call ID: d07f2d3b-38b1-49f2-bf06-ce7fbbb5b391
  Args:
    type: :Man
    source: Alfonso_XIII_of_Spain
  AssignClass (f7723b3b-5cbb-48b4-bb8e-72b27626b9a1)
 Call ID: f7723b3b-5cbb-48b4-bb8e-72b27626b9a1
  Args:
    type: :Man
    source: Gonzalo_Maria_de_Ulloa_y_Ramírez_de_Haro
  AddTriple (88bd0379-f704-49a0-b8d7-c4283a3e048a)
 Call ID: 88bd0379-f704-49a0-b8d7-c4283a3e048a
  Args:
    target: Gonzalo_Maria_de_Ulloa_y_Ramírez_de_Haro
    relation: :hasFather
    source: Doña_María_del_Carmen_de_Ulloa_y_Suelves
  AssignClass (fe1d97cd-d58e-4f68-aff4-6509998488ae)
 Call ID: fe1d97cd-d58e-4f68-aff4-6509998488ae
  Args:
    type: :Woman
    source: Françoise_Cazaudehore
  AddTriple (4c3d27f5-21e2-4706-a137-001a1d1dfe46)
 Call ID: 4c3d27f5-21e2-4706-a137-001a1d1dfe46
  Args:
    source: Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasRelation
    target: Françoise_Cazaudehore
  AssignClass (76220ec2-f875-4391-afe3-5fd5d53faa5b)
 Call ID: 76220ec2-f875-4391-afe3-5fd5d53faa5b
  Args:
    type: :Woman
    source: Kristine_Dzidziguri
  AddTriple (07d92aac-cc3c-4a16-bfde-fcd37b495a06)
 Call ID: 07d92aac-cc3c-4a16-bfde-fcd37b495a06
  Args:
    target: Kristine_Dzidziguri
    relation: :hasRelation
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
  AddLiteral (5c16a038-09b0-432e-99fb-ef70aa7a9758)
 Call ID: 5c16a038-09b0-432e-99fb-ef70aa7a9758
  Args:
    relation: :hasMarriageYear
    source: Prince_Juan_Jorge_de_Bagration-Mukhrani
    literal_type: xsd:integer
    literal_value: 2014
  Finish (d2f916aa-0b05-4af9-aa77-631f048fe9ed)
 Call ID: d2f916aa-0b05-4af9-aa77-631f048fe9ed
  Args: