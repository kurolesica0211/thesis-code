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
Nicholas Michael de Roumanie Medforth-Mills (born 1 April 1985), formerly known as Prince Nicholas of Romania, is the eldest child and only son of Princess Elena of Romania and Robin Medforth-Mills.
As a grandson of King Michael of Romania, he was third in line to the defunct throne of Romania according to a new family statute enacted in 2007, that also conferred the title of a "prince of Romania" on him which was removed in 2015.
Early life

Birth

Nicholas de Roumanie Medforth-Mills was born on 1 April 1985 at La Tour Hospital in Meyrin, a commuter town near Geneva, Switzerland, the first child and son of Princess Elena of Romania and her first husband Robin Medforth-Mills and the second grandchild of King Michael I of Romania and his wife Queen Anne.
He was baptized in the Orthodox faith, his godparents being Queen Anne (his maternal grandmother) and Crown Princess Margareta of Romania (his maternal aunt).
Childhood

Until the age of four, Medforth-Mills lived with his sister and parents at the Romanian royal family's residence in Versoix, Switzerland.
Medforth-Mills joined the Beaver Scouts at age five.
During his childhood, he developed an interest in cars, an interest shared with his grandfather King Michael I.
During holidays in Versoix, Switzerland, with his maternal grandparents, Nicholas spent hours in his grandfather's garage, watching him maintain his Jeep collection.
In an interview with historian Filip-Lucian Iorga, Nicholas recalled the time spent with King Michael, and how he had been allowed to drive one of his cars, a Ford which once belonged to General George S. Patton; the vehicle was given to his grandfather by Queen Anne's paternal uncle Prince Felix of Bourbon-Parma as a gift.
He also recalled spending time with Queen Anne at Versoix where they used to fish and play golf together.
As a descendant of Queen Victoria of the United Kingdom and King Christian IX of Denmark, he regularly met with many of his extended relatives.
Education

Medforth-Mills attended Argyle House School, Sunderland, England which he left in 1999 with eight GCSEs - English Language, English Literature, Mathematics, Science (Chemistry, Biology and Physics), French, German, Information Technology, and Geography.
Before enrolling for university he took a five-year "Gap year", where:


Activities in Romania

Nicholas’s first major appearance in Romania was on 19 April 1992 on Easter Day along with his grandparents
King Michael
I and Queen Anne and with his mother and her second husband Alexander Nixon.
Nicholas came again for the second time on Christmas Day 1997, when the entire royal family set foot in Romania for the first time after nearly five decades of exile.
In 2002, he visited Romania for the third time; he stayed at Elisabeta Palace.
In 2008, de Roumanie Medforth-Mills became more involved in the public life of Romania, taking part, for instance, at the 2008 UNITER theatre gala and in visits throughout the country with his aunt, Crown Princess Margareta, and  Radu Duda.
Royal status

Prince of Romania

In 1997, Romanian monarchists intended to ask Michael to designate a male heir-presumptive from the House of Hohenzollern in keeping with the rules of the last royal constitution which were based on agnatic primogeniture and Salic law.
The monarchists eventually agreed on a compromise and requested him to designate a male rather than female heir-presumptive, in the person of Nicholas.
However, under the influence of Queen Anne, Michael rejected the monarchists' request, and at the end of 1997, he designated Princess Margareta as heir presumptive in keeping with the European Convention on Human Rights, which meant Nicholas would only succeed to the headship of the royal family after the deaths of King Michael, Crown Princess Margareta and his mother.
In 2005, King Michael told Nicholas that he could choose to have the chance of becoming a "prince of Romania" which would mean assuming responsibility in a conscious manner by starting to work for the country.
On 30 December 2007, the press office of King Michael announced that Nicholas de Roumanie Medforth-Mills would receive the title "prince of Romania" with the style of "royal highness", coming into effect on Nicholas's 25th birthday.
In February 2008, Nicholas stated in an interview with the Romanian daily newspaper Cotidianul that if the Romanian people asked him to become king, he would not refuse.
In September 2012, after his university studies, he moved to Romania to undertake more of the royal family's public activities.
Removal of titles and illegitimate daughter

On 1 August 2015, former King Michael of Romania signed a document removing the title prince of Romania and the qualification of royal highness from his grandson.
Medforth-Mills also has been removed from the line of succession, as defined by his grandfather.
The former king took the decision after considering that Romania needed a ruler marked by modesty and moral principles, respect and thought for others after the "reign and life" of his eldest daughter, Crown Princess Margareta, will have finished.
In issuing the declaration, the former king expressed the hope that "Nicholas will find in future years a suitable way to serve the ideals and use the qualities that God gave him".
Nicholas's mother, Princess Elena, received notification of the former king's decision in a personal letter.
The validity of the document has been challenged by Nicholas who has stated there was no signature whatsoever from King Michael.
The move "stunned Romanians" and "sparked speculation that a jealous relative had sought to edge Nicholas out of the succession."
The exclusion of Nicholas from the royal succession was due to the birth of an illegitimate daughter, from a short relationship with Nicoleta Cîrjan.
Nicholas released a press statement on 18 November 2017 from London about the child.
Point 2 of the Press release stated, that on learning of the pregnancy, "I returned to Romania in November 2015 to resolve the situation with my alleged child.
On 27 May 2019, Nicholas confirmed via a Facebook post that paternity tests had confirmed the illegitimate daughter is his, and that he had assumed legal responsibility for her.
Allegation of assault

On 8 November 2017, during Michael I's final illness, Crown Princess Margareta filed a complaint with Swiss police alleging that Nicholas tried to force his way into his grandfather's home.
It alleged that Nicholas "physically and verbally assaulted" three staff members, while he accused his relatives of trying to stop him seeing his grandfather and discrediting his name.
Nicholas was acquitted of all charges by the court of Nyon in October 2021.
Marriage

Nicholas married civilly in Henley-on-Thames on 6 October 2017 to Alina-Maria Binder (born in Constanța on 26 January 1988).



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
  AssignClass (4f1cb1f7-ea48-46a4-8345-caf7b253fbc0)
 Call ID: 4f1cb1f7-ea48-46a4-8345-caf7b253fbc0
  Args:
    type: :Man
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
  AssignClass (82aa523e-a986-4c8a-a542-0ebea7bc87ce)
 Call ID: 82aa523e-a986-4c8a-a542-0ebea7bc87ce
  Args:
    type: :Woman
    source: Princess_Elena_of_Romania
  AssignClass (c3fe6e7c-4467-4d93-8480-3093fb8acd16)
 Call ID: c3fe6e7c-4467-4d93-8480-3093fb8acd16
  Args:
    type: :Man
    source: Robin_Medforth-Mills
  AssignClass (08ecab7f-b0e2-40e1-a8c5-2008e8008b97)
 Call ID: 08ecab7f-b0e2-40e1-a8c5-2008e8008b97
  Args:
    type: :Man
    source: King_Michael_I_of_Romania
  AssignClass (65581b41-bbff-45b0-8b70-98d7c3b1ba7b)
 Call ID: 65581b41-bbff-45b0-8b70-98d7c3b1ba7b
  Args:
    type: :Woman
    source: Queen_Anne
  AssignClass (2bb4e04b-27b1-47ae-8060-2679b9651e77)
 Call ID: 2bb4e04b-27b1-47ae-8060-2679b9651e77
  Args:
    type: :Woman
    source: Crown_Princess_Margareta_of_Romania
  AssignClass (1c5edaba-9d2a-423b-b1a6-679e8226bd37)
 Call ID: 1c5edaba-9d2a-423b-b1a6-679e8226bd37
  Args:
    type: :Woman
    source: Alina-Maria_Binder
  AssignClass (95eb48b0-2590-4ad0-8945-d0e9300abbb2)
 Call ID: 95eb48b0-2590-4ad0-8945-d0e9300abbb2
  Args:
    type: :Woman
    source: Nicoleta_Cîrjan
  AddLiteral (f0986e3c-053a-438e-abf5-c1ea56968368)
 Call ID: f0986e3c-053a-438e-abf5-c1ea56968368
  Args:
    relation: :knownAs
    literal_value: Nicholas Michael de Roumanie Medforth-Mills
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    literal_type: xsd:string
  AddLiteral (05bff35e-1fe8-4ea0-8f55-7235cdde2d68)
 Call ID: 05bff35e-1fe8-4ea0-8f55-7235cdde2d68
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    literal_type: xsd:string
    relation: :formerlyKnownAs
    literal_value: Prince Nicholas of Romania
  AddTriple (a460924e-e334-44b2-8b72-bd3126058152)
 Call ID: a460924e-e334-44b2-8b72-bd3126058152
  Args:
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    relation: :hasFather
    target: Robin_Medforth-Mills
  AddTriple (12888c70-3b42-4df4-978a-280c16958ed6)
 Call ID: 12888c70-3b42-4df4-978a-280c16958ed6
  Args:
    relation: :hasMother
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    target: Princess_Elena_of_Romania
  AddTriple (a23bfd40-3b69-44cf-99ee-8d7a99923ac2)
 Call ID: a23bfd40-3b69-44cf-99ee-8d7a99923ac2
  Args:
    relation: :hasFather
    source: Princess_Elena_of_Romania
    target: King_Michael_I_of_Romania
  AddTriple (f4e097ab-42d1-4bb8-ad84-0956bde2d785)
 Call ID: f4e097ab-42d1-4bb8-ad84-0956bde2d785
  Args:
    relation: :hasMother
    source: Princess_Elena_of_Romania
    target: Queen_Anne
  AddTriple (a2473596-a68e-40dc-8f93-9660017ed962)
 Call ID: a2473596-a68e-40dc-8f93-9660017ed962
  Args:
    source: Queen_Anne
    relation: :isMotherOf
    target: Princess_Elena_of_Romania
  AddTriple (6ae4ed0f-29cf-46a1-9c8d-e326a6f9c4f0)
 Call ID: 6ae4ed0f-29cf-46a1-9c8d-e326a6f9c4f0
  Args:
    source: King_Michael_I_of_Romania
    relation: :isFatherOf
    target: Princess_Elena_of_Romania
  AddTriple (bf21dd8a-4ca9-4a75-8ae5-13eb4aa2a621)
 Call ID: bf21dd8a-4ca9-4a75-8ae5-13eb4aa2a621
  Args:
    relation: :isSisterOf
    source: Crown_Princess_Margareta_of_Romania
    target: Princess_Elena_of_Romania
  AddTriple (3d23c9e7-d398-4ac1-ac28-9e8813cac147)
 Call ID: 3d23c9e7-d398-4ac1-ac28-9e8813cac147
  Args:
    target: Crown_Princess_Margareta_of_Romania
    relation: :isMotherOf
    source: Queen_Anne
  AddTriple (2bf1c7d5-e6c6-453c-99eb-251df777d7b9)
 Call ID: 2bf1c7d5-e6c6-453c-99eb-251df777d7b9
  Args:
    source: King_Michael_I_of_Romania
    relation: :isFatherOf
    target: Crown_Princess_Margareta_of_Romania
  AddTriple (1359a915-d629-464b-b8f2-e464190470f6)
 Call ID: 1359a915-d629-464b-b8f2-e464190470f6
  Args:
    target: King_Michael_I_of_Romania
    source: Crown_Princess_Margareta_of_Romania
    relation: :hasFather
  AddTriple (70b227c5-bcc6-4c52-afaf-d5d65433dfa2)
 Call ID: 70b227c5-bcc6-4c52-afaf-d5d65433dfa2
  Args:
    source: Crown_Princess_Margareta_of_Romania
    relation: :hasMother
    target: Queen_Anne
  AddTriple (7abdba88-2d52-4530-8f2c-47f055e46b00)
 Call ID: 7abdba88-2d52-4530-8f2c-47f055e46b00
  Args:
    relation: :isFatherOf
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    target: Unnamed_Daughter_of_Nicholas_and_Nicoleta_Cîrjan
  AddTriple (03a1128a-ce3f-4837-bb35-9de4b0368677)
 Call ID: 03a1128a-ce3f-4837-bb35-9de4b0368677
  Args:
    target: Unnamed_Daughter_of_Nicholas_and_Nicoleta_Cîrjan
    relation: :isMotherOf
    source: Nicoleta_Cîrjan
  AssignClass (a9e849c2-48da-42e4-976c-891711a96b79)
 Call ID: a9e849c2-48da-42e4-976c-891711a96b79
  Args:
    type: :Woman
    source: Unnamed_Daughter_of_Nicholas_and_Nicoleta_Cîrjan
  AddTriple (35a30676-771b-4f7b-9bdc-eef10a1db02d)
 Call ID: 35a30676-771b-4f7b-9bdc-eef10a1db02d
  Args:
    target: Alina-Maria_Binder
    source: Nicholas_Michael_de_Roumanie_Medforth-Mills
    relation: :hasRelation
  Finish (9e770304-4072-4b6b-b823-d58493a4abe9)
 Call ID: 9e770304-4072-4b6b-b823-d58493a4abe9
  Args: