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

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

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

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

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



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (fadb805e-f861-4cfc-bdc5-a7cb5d921551)
 Call ID: fadb805e-f861-4cfc-bdc5-a7cb5d921551
  Args:
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
    type: :Man
  AssignClass (b773175f-0aa8-47ac-8418-ad4668400452)
 Call ID: b773175f-0aa8-47ac-8418-ad4668400452
  Args:
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
    type: :Person
  AddLiteral (4b058aa8-29e0-4d8e-9c95-a12e081d3758)
 Call ID: 4b058aa8-29e0-4d8e-9c95-a12e081d3758
  Args:
    literal_value: 1977
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
  AssignClass (8f556251-f478-46d2-b753-61bcc77c9b01)
 Call ID: 8f556251-f478-46d2-b753-61bcc77c9b01
  Args:
    source: :Prince_Bagrat_de_Bagration_y_de_Baviera
    type: :Man
  AssignClass (37ba28d9-8211-49bc-b029-615b07e98f50)
 Call ID: 37ba28d9-8211-49bc-b029-615b07e98f50
  Args:
    source: :Prince_Bagrat_de_Bagration_y_de_Baviera
    type: :Person
  AssignClass (09198063-1cf6-47e1-991c-b063a114befe)
 Call ID: 09198063-1cf6-47e1-991c-b063a114befe
  Args:
    source: :Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    type: :Woman
  AssignClass (108a9f01-9cf7-4e64-b8fc-96dcf480d8ff)
 Call ID: 108a9f01-9cf7-4e64-b8fc-96dcf480d8ff
  Args:
    type: :Person
    source: :Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
  AddTriple (0c850b3f-a530-40cb-9dcf-afaa203ade7e)
 Call ID: 0c850b3f-a530-40cb-9dcf-afaa203ade7e
  Args:
    relation: :hasFather
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
    target: :Prince_Bagrat_de_Bagration_y_de_Baviera
  AddTriple (75ff13f1-645c-4828-99f8-4d82df6e8c62)
 Call ID: 75ff13f1-645c-4828-99f8-4d82df6e8c62
  Args:
    relation: :hasMother
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
    target: :Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
  AssignClass (03c5f017-d554-471c-bd84-d388f61008fd)
 Call ID: 03c5f017-d554-471c-bd84-d388f61008fd
  Args:
    type: :Man
    source: :Prince_Irakli_Bagration_of_Mukhrani
  AssignClass (d3d18048-16a5-4237-8dab-fc2a7ef3ae23)
 Call ID: d3d18048-16a5-4237-8dab-fc2a7ef3ae23
  Args:
    source: :Prince_Irakli_Bagration_of_Mukhrani
    type: :Person
  AddTriple (16677561-5205-4368-82d8-75499c7558e6)
 Call ID: 16677561-5205-4368-82d8-75499c7558e6
  Args:
    target: :Prince_Irakli_Bagration_of_Mukhrani
    relation: :hasFather
    source: :Prince_Bagrat_de_Bagration_y_de_Baviera
  AssignClass (5f96ef7b-2745-4f18-b290-879fb037d2d0)
 Call ID: 5f96ef7b-2745-4f18-b290-879fb037d2d0
  Args:
    source: :Infanta_Maria_de_las_Mercedes_of_Spain
    type: :Woman
  AssignClass (2065ba8d-27c9-49ab-8463-637a1aac77a8)
 Call ID: 2065ba8d-27c9-49ab-8463-637a1aac77a8
  Args:
    type: :Person
    source: :Infanta_Maria_de_las_Mercedes_of_Spain
  AddTriple (69c34692-e7c5-4f0a-97cc-ea468fa8423c)
 Call ID: 69c34692-e7c5-4f0a-97cc-ea468fa8423c
  Args:
    target: :Infanta_Maria_de_las_Mercedes_of_Spain
    source: :Prince_Bagrat_de_Bagration_y_de_Baviera
    relation: :hasMother
  AssignClass (28e6aba0-4d9a-436a-9dac-7594911de299)
 Call ID: 28e6aba0-4d9a-436a-9dac-7594911de299
  Args:
    type: :Man
    source: :Prince_Ferdinand_of_Bavaria
  AssignClass (114b4696-541f-4942-ad56-9957a7dae918)
 Call ID: 114b4696-541f-4942-ad56-9957a7dae918
  Args:
    source: :Prince_Ferdinand_of_Bavaria
    type: :Person
  AddTriple (0f011952-4ce1-49e6-80f0-911d88beff54)
 Call ID: 0f011952-4ce1-49e6-80f0-911d88beff54
  Args:
    relation: :hasFather
    source: :Infanta_Maria_de_las_Mercedes_of_Spain
    target: :Prince_Ferdinand_of_Bavaria
  AssignClass (59ccf60c-68ce-42ae-b794-748f5cc37979)
 Call ID: 59ccf60c-68ce-42ae-b794-748f5cc37979
  Args:
    type: :Man
    source: :Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
  AssignClass (5312a66f-10cd-4a6c-ab8f-c366cf8ee4ac)
 Call ID: 5312a66f-10cd-4a6c-ab8f-c366cf8ee4ac
  Args:
    source: :Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
    type: :Person
  AddTriple (fadaf702-9fa1-46af-84e5-6d8441f177f8)
 Call ID: fadaf702-9fa1-46af-84e5-6d8441f177f8
  Args:
    relation: :hasFather
    source: :Dona_Maria_del_Carmen_de_Ulloa_y_Suelves
    target: :Gonzalo_Maria_de_Ulloa_y_Ramirez_de_Haro
  AssignClass (a8649526-43ce-423b-9bbd-2ff81f8cc3ed)
 Call ID: a8649526-43ce-423b-9bbd-2ff81f8cc3ed
  Args:
    type: :Woman
    source: :Francoise_Cazaudehore
  AssignClass (bd836a4a-f7d0-4e84-94cb-e513d7b5c71c)
 Call ID: bd836a4a-f7d0-4e84-94cb-e513d7b5c71c
  Args:
    source: :Francoise_Cazaudehore
    type: :Person
  AssignClass (fa53ddf2-7fc4-47dd-8d17-ab1714bfcad1)
 Call ID: fa53ddf2-7fc4-47dd-8d17-ab1714bfcad1
  Args:
    type: :Woman
    source: :Princess_Kristine_Dzidziguri
  AssignClass (eb8cb0c9-0e6f-48c2-b868-80d66f34d863)
 Call ID: eb8cb0c9-0e6f-48c2-b868-80d66f34d863
  Args:
    type: :Person
    source: :Princess_Kristine_Dzidziguri
  AddLiteral (e5deb30f-6f50-4610-999e-ceb232a6dfb4)
 Call ID: e5deb30f-6f50-4610-999e-ceb232a6dfb4
  Args:
    literal_type: xsd:integer
    literal_value: 2014
    relation: :hasMarriageYear
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
  AddTriple (a44e3491-d100-4d98-b4ad-a4e97f831db3)
 Call ID: a44e3491-d100-4d98-b4ad-a4e97f831db3
  Args:
    target: :Princess_Kristine_Dzidziguri
    relation: :hasRelation
    source: :Prince_Juan_Jorge_de_Bagration-Mukhrani
  Finish (19780116-04e2-4e6e-bda0-926947022196)
 Call ID: 19780116-04e2-4e6e-bda0-926947022196
  Args: