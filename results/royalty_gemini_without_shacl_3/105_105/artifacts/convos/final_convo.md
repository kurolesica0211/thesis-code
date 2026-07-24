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
The Duke of Castro  The Duchess of Castro


Prince Carlo of Bourbon-Two Sicilies, Duke of Castro (born 24 February 1963) is one of two claimants to the headship of the House of Bourbon-Two Sicilies.
Early life

Prince Carlo was born in Saint-Raphaël, Var, France, the only son of Prince Ferdinand, Duke of Castro and Chantal de Chevron-Villette.
Marriage and issue

Prince Carlo married Camilla Crociani, daughter of Italian billionaire Camillo Crociani and his second wife, Italian actress Edy Vessel, on 31 October 1998 at the Cathedral of Our Lady Immaculate in the Monaco-Ville ward of Monaco.
The couple were introduced to each other by Albert II, Prince of Monaco.
Notable guests at the wedding included Rainier III, Prince of Monaco, Albert, Hereditary Prince of Monaco (later Prince Albert II of Monaco), and Prince Laurent of Belgium.
Together Carlo and Camilla have two daughters:


Prince Carlo is also a godfather to Princess Josephine of Denmark, the youngest child of King Frederik X and Queen Mary of Denmark, and attended her confirmation in 2026.
He and Princess Camilla are regarded as close friends of the Danish King and Queen.
Claimed headship of the House of Bourbon-Two Sicilies

In 2008, Carlo succeeded to his father's claim as head of the House of the Two Sicilies and the use of the title Duke of Castro.
Carlos married María de las Mercedes, Princess of Asturias, the heir presumptive of Spain, in 1901.
Alfonso's line of the family (today represented by Carlo's rival claimant, Pedro) has been officially recognized as the legitimate line by the Government of Spain, the Spanish royal house, the Parmesan royal house and the Portuguese royal house, whereas Ranieri's line was recognized by many non-ruling European dynasts of former monarchies (no current monarch except the king of Spain has officially stated its view on the matter), namely the Count of Paris, Umberto of Italy, Gottfried of Austria-Tuscany, the Duke of Bavaria, the Duke of Württemberg, the Duke of Aosta, the Duke of Genoa, the Duke of Hohenberg, Prince Luiz of Orléans-Braganza and Prince Michael of Greece, as well as all other members of the Sicilian house itself.
It has been argued by some that the Counts of Paris supported the Castro line simply because their own pretence to the French throne depends entirely on the same principle of renunciation as the Act of Cannes, and so it would be against their own interest to support the Calabrian line.
Interestingly, most of the other outspoken supporters of the Castro line were either sons-in-law of the Count of Paris or closely related to him.
Honours

Dynastic

Ecclesiastical

National

Foreign

In letters dated 21 July 2017, the Governor-General of Antigua and Barbuda issued a notice that the Duke of Castro's 2014 appointment to the Order of the Nation had been annulled.
In 2020, the branch of the Constantinian Order led by Prince Carlo was alleged to have influenced the election of Patricia Scotland as Commonwealth Secretary-General, which a spokesman for the Order denied, saying "These allegations are wholly offensive and wrong".



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
  AssignClass (334ecf8e-18b5-4b75-99ca-104d59067908)
 Call ID: 334ecf8e-18b5-4b75-99ca-104d59067908
  Args:
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (1393aab2-6f63-44a9-8211-c15dc939b882)
 Call ID: 1393aab2-6f63-44a9-8211-c15dc939b882
  Args:
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    type: :Person
  AddLiteral (8ec2545d-6899-48c9-ba10-fc2579268f80)
 Call ID: 8ec2545d-6899-48c9-ba10-fc2579268f80
  Args:
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    relation: :hasBirthYear
    literal_value: 1963
    literal_type: xsd:integer
  AssignClass (1da0f75b-4ca4-4dd0-b106-523556232f8f)
 Call ID: 1da0f75b-4ca4-4dd0-b106-523556232f8f
  Args:
    type: :Man
    source: Prince_Ferdinand_Duke_of_Castro
  AssignClass (906ffde1-d1a2-49dc-8f3d-33d8fa905851)
 Call ID: 906ffde1-d1a2-49dc-8f3d-33d8fa905851
  Args:
    source: Prince_Ferdinand_Duke_of_Castro
    type: :Person
  AssignClass (64e7e5d6-97b3-4c5b-808f-06c934aa1ac6)
 Call ID: 64e7e5d6-97b3-4c5b-808f-06c934aa1ac6
  Args:
    type: :Woman
    source: Chantal_de_Chevron-Villette
  AssignClass (d9c11f1e-2810-4060-ac42-0d4be05ee7a3)
 Call ID: d9c11f1e-2810-4060-ac42-0d4be05ee7a3
  Args:
    source: Chantal_de_Chevron-Villette
    type: :Person
  AddTriple (8a422d02-6d8a-4635-874a-2afcc9c2dae8)
 Call ID: 8a422d02-6d8a-4635-874a-2afcc9c2dae8
  Args:
    target: Prince_Ferdinand_Duke_of_Castro
    relation: :hasFather
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
  AddTriple (98b0f4d9-5cc1-4060-a510-310fe2fe6ebc)
 Call ID: 98b0f4d9-5cc1-4060-a510-310fe2fe6ebc
  Args:
    target: Chantal_de_Chevron-Villette
    relation: :hasMother
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
  AssignClass (72ee3f74-bb26-460f-b4e8-e189f981c3fb)
 Call ID: 72ee3f74-bb26-460f-b4e8-e189f981c3fb
  Args:
    source: Camilla_Crociani
    type: :Woman
  AssignClass (98dafc7c-da1e-4cac-86b9-078b866a9e74)
 Call ID: 98dafc7c-da1e-4cac-86b9-078b866a9e74
  Args:
    type: :Person
    source: Camilla_Crociani
  AddTriple (20551d54-f41c-479c-a26d-0f0e1b500061)
 Call ID: 20551d54-f41c-479c-a26d-0f0e1b500061
  Args:
    relation: :hasRelation
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
    target: Camilla_Crociani
  AddLiteral (a0c780d5-382a-42ba-95c3-2de320eaeb57)
 Call ID: a0c780d5-382a-42ba-95c3-2de320eaeb57
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1998
    source: Prince_Carlo_of_Bourbon-Two_Sicilies
  AssignClass (2a4abbb4-865a-4589-9707-906fb7b377c4)
 Call ID: 2a4abbb4-865a-4589-9707-906fb7b377c4
  Args:
    type: :Man
    source: Camillo_Crociani
  AssignClass (44d976ee-96bd-4759-a2fb-d2177cc2e9f0)
 Call ID: 44d976ee-96bd-4759-a2fb-d2177cc2e9f0
  Args:
    source: Camillo_Crociani
    type: :Person
  AssignClass (a7e9c852-517a-4baf-af7e-93f85d8239b8)
 Call ID: a7e9c852-517a-4baf-af7e-93f85d8239b8
  Args:
    source: Edy_Vessel
    type: :Woman
  AssignClass (aabb3af5-9967-493b-801f-977108864cfa)
 Call ID: aabb3af5-9967-493b-801f-977108864cfa
  Args:
    source: Edy_Vessel
    type: :Person
  AddTriple (4bd9eed2-4b26-47ce-bb53-6aca5632152e)
 Call ID: 4bd9eed2-4b26-47ce-bb53-6aca5632152e
  Args:
    relation: :hasFather
    source: Camilla_Crociani
    target: Camillo_Crociani
  AddTriple (2fca2415-df2a-4f7e-935b-16b69b456bd5)
 Call ID: 2fca2415-df2a-4f7e-935b-16b69b456bd5
  Args:
    target: Edy_Vessel
    source: Camilla_Crociani
    relation: :hasMother
  AssignClass (07721067-db2a-4077-bfa6-46a848fb56b5)
 Call ID: 07721067-db2a-4077-bfa6-46a848fb56b5
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Man
  AssignClass (d56ee575-cc63-4e47-937c-60044a7bd7c0)
 Call ID: d56ee575-cc63-4e47-937c-60044a7bd7c0
  Args:
    source: Carlos_of_Bourbon-Two_Sicilies
    type: :Person
  AssignClass (7e49439e-0ac1-4473-a889-2cbd12783993)
 Call ID: 7e49439e-0ac1-4473-a889-2cbd12783993
  Args:
    type: :Woman
    source: Maria_de_las_Mercedes_Princess_of_Asturias
  AssignClass (b2647001-9b9f-4b85-9cbc-0df308df15ea)
 Call ID: b2647001-9b9f-4b85-9cbc-0df308df15ea
  Args:
    source: Maria_de_las_Mercedes_Princess_of_Asturias
    type: :Person
  AddTriple (0b6944f4-5a85-4763-aa1a-ef11373fb322)
 Call ID: 0b6944f4-5a85-4763-aa1a-ef11373fb322
  Args:
    target: Maria_de_las_Mercedes_Princess_of_Asturias
    source: Carlos_of_Bourbon-Two_Sicilies
    relation: :hasRelation
  AddLiteral (764374b4-f420-45e3-b648-889a2d46497f)
 Call ID: 764374b4-f420-45e3-b648-889a2d46497f
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1901
    source: Carlos_of_Bourbon-Two_Sicilies
  Finish (1555ee77-a91b-4f8d-bfd8-519c6ded6a9d)
 Call ID: 1555ee77-a91b-4f8d-bfd8-519c6ded6a9d
  Args: