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
Duke John Albert of Mecklenburg (German: Herzog Johann Albrecht zu Mecklenburg; given names John Albert Ernest Constantine Frederick Henry; 8 December 1857 – 16 February 1920) was a member of the House of Mecklenburg-Schwerin who served as the regent of two states of the German Empire.
He was first regent of the Grand Duchy of Mecklenburg-Schwerin from 1897 to 1901 for his nephew Frederick Francis IV, Grand Duke of Mecklenburg, and thereafter regent of the Duchy of Brunswick from 1907 to 1913.
Birth and interests

Duke John Albert of Mecklenburg was born in Schwerin the fifth child of Frederick Francis II, Grand Duke of Mecklenburg and his first wife Princess Augusta Reuss of Köstritz (1822–1862).
Duke John Albert was educated in Dresden, pursued a career in the Prussian Army and was well known for his love of sports.
Regencies

Following the death of his brother Frederick Francis III, Grand Duke of Mecklenburg on 10 April 1897, Duke John Albert was appointed regent for his young nephew the new Grand Duke, Frederick Francis IV after his older brother Duke Paul Frederick had renounced his claim to the regency.
On 28 May 1907, Duke John Albert was elected regent of the Duchy of Brunswick following the death of Prince Albert of Prussia by the state's diet, accepting the offer he arrived in Brunswick on 5 June 1907.
The reason for the regency in Brunswick was that in 1884 when William, Duke of Brunswick died his distant cousin and heir Ernest Augustus, Crown Prince of Hanover was prevented from taking over the duchy because he refused to renounce his claim to the throne of the Kingdom of Hanover which had been annexed by Prussia in 1866.
Shortly after assuming the regency, Duke John Albert would walk Brunswick in civilian clothes visiting museums, libraries and other institutions in the duchy, asking questions of people to discover their living conditions.
Duke John Albert also cut down on the expenses of the royal household by cutting the number of servants and retainers to the minimum needed to run the household.
The regency came to an end on 1 November 1913 when Ernest Augustus, Crown Prince of Hanover's son Ernest Augustus was permitted to ascend to Duchy following his marriage to Princess Victoria Louise of Prussia, the only daughter of the German Emperor, William II, which helped heal the rift between the houses of Hanover and Hohenzollern.
War years

During the First World War, Duke John Albert was active with the German Colonial Society in defending Germany's colonial possessions from suggestions that they should be abandoned.
Duke John Albert died in 1920 in Wiligrad castle near Lübstorf aged 62.
Marriages

John Albert was married twice: firstly in Weimar on 6 November 1886 to Princess Elisabeth Sybille of Saxe-Weimar-Eisenach (28 February 1854–10 July 1908)
the daughter of Charles Alexander, Grand Duke of Saxe-Weimar-Eisenach; secondly in Brunswick on 15 December 1909 to Princess Elisabeth of Stolberg-Rossla (1885–1969), who following his death was to marry his half brother Duke Adolf Friedrich in 1924.
Ojimukoka

Ojimukoka, a small settlement, postoffice and railway station in Namibia, was renamed Johann - Albrechtshöhe, and then simply Albrechts in his honour.



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
  AssignClass (d58dd058-6483-467d-b9b4-8c761caf1681)
 Call ID: d58dd058-6483-467d-b9b4-8c761caf1681
  Args:
    type: :Man
    source: Duke_John_Albert_of_Mecklenburg
  AssignClass (77fc3772-b2e3-42ad-90cc-2d6152fe0e9d)
 Call ID: 77fc3772-b2e3-42ad-90cc-2d6152fe0e9d
  Args:
    source: Duke_John_Albert_of_Mecklenburg
    type: :Person
  AddLiteral (7a56f69e-5f40-4af7-8ee0-36b24cd8ab53)
 Call ID: 7a56f69e-5f40-4af7-8ee0-36b24cd8ab53
  Args:
    literal_type: xsd:integer
    source: Duke_John_Albert_of_Mecklenburg
    relation: :hasBirthYear
    literal_value: 1857
  AddLiteral (2c446050-5707-4e5b-a215-7392f5dd0bbf)
 Call ID: 2c446050-5707-4e5b-a215-7392f5dd0bbf
  Args:
    literal_type: xsd:integer
    source: Duke_John_Albert_of_Mecklenburg
    literal_value: 1920
    relation: :hasDeathYear
  AssignClass (a72a4c5c-357f-492d-a03b-0aa60fa1aace)
 Call ID: a72a4c5c-357f-492d-a03b-0aa60fa1aace
  Args:
    source: Frederick_Francis_II_Grand_Duke_of_Mecklenburg
    type: :Man
  AssignClass (b757d444-b618-4f68-96b8-d7a0c07cd6cd)
 Call ID: b757d444-b618-4f68-96b8-d7a0c07cd6cd
  Args:
    type: :Person
    source: Frederick_Francis_II_Grand_Duke_of_Mecklenburg
  AssignClass (05ec82ae-acd9-4bf8-b724-7e74fd4f41e4)
 Call ID: 05ec82ae-acd9-4bf8-b724-7e74fd4f41e4
  Args:
    source: Princess_Augusta_Reuss_of_Köstritz
    type: :Woman
  AssignClass (d43ab075-993f-477d-aa0a-8d24e8ea38d4)
 Call ID: d43ab075-993f-477d-aa0a-8d24e8ea38d4
  Args:
    type: :Person
    source: Princess_Augusta_Reuss_of_Köstritz
  AddTriple (57c72da9-a9f6-43e7-a8ef-a834ea63665b)
 Call ID: 57c72da9-a9f6-43e7-a8ef-a834ea63665b
  Args:
    source: Duke_John_Albert_of_Mecklenburg
    target: Frederick_Francis_II_Grand_Duke_of_Mecklenburg
    relation: :hasFather
  AddTriple (8054eb9b-8a44-4dba-a52b-6c7c561676a8)
 Call ID: 8054eb9b-8a44-4dba-a52b-6c7c561676a8
  Args:
    source: Duke_John_Albert_of_Mecklenburg
    relation: :hasMother
    target: Princess_Augusta_Reuss_of_Köstritz
  AssignClass (1014b8ce-b35b-400f-b6ce-66a2adaa9038)
 Call ID: 1014b8ce-b35b-400f-b6ce-66a2adaa9038
  Args:
    type: :Man
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg
  AssignClass (256845a1-4c19-4d64-b1e8-e4a3216246e3)
 Call ID: 256845a1-4c19-4d64-b1e8-e4a3216246e3
  Args:
    type: :Person
    source: Frederick_Francis_III_Grand_Duke_of_Mecklenburg
  AddTriple (7f9a5bd3-25b0-49b8-be7a-3d322be02721)
 Call ID: 7f9a5bd3-25b0-49b8-be7a-3d322be02721
  Args:
    source: Duke_John_Albert_of_Mecklenburg
    relation: :hasBrother
    target: Frederick_Francis_III_Grand_Duke_of_Mecklenburg
  AssignClass (eea3e41f-0818-4131-86a9-b183597477fb)
 Call ID: eea3e41f-0818-4131-86a9-b183597477fb
  Args:
    type: :Man
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg
  AssignClass (e6d603c2-aefc-4b65-b939-b45db368b80d)
 Call ID: e6d603c2-aefc-4b65-b939-b45db368b80d
  Args:
    source: Frederick_Francis_IV_Grand_Duke_of_Mecklenburg
    type: :Person
  AssignClass (e6bc4bd3-fff6-495e-8acd-a11e6f79025a)
 Call ID: e6bc4bd3-fff6-495e-8acd-a11e6f79025a
  Args:
    source: Duke_Paul_Frederick
    type: :Man
  AssignClass (9845a148-df9d-4f74-b1cf-6a25c62155ac)
 Call ID: 9845a148-df9d-4f74-b1cf-6a25c62155ac
  Args:
    type: :Person
    source: Duke_Paul_Frederick
  AddTriple (b73d8132-6486-4e6a-9651-03a4c213e034)
 Call ID: b73d8132-6486-4e6a-9651-03a4c213e034
  Args:
    source: Duke_John_Albert_of_Mecklenburg
    target: Duke_Paul_Frederick
    relation: :hasBrother
  AssignClass (384d9c9b-e933-4c7f-ac06-43f4e919196f)
 Call ID: 384d9c9b-e933-4c7f-ac06-43f4e919196f
  Args:
    type: :Woman
    source: Princess_Elisabeth_Sybille_of_Saxe_Weimar_Eisenach
  AssignClass (93429e6d-044e-4c34-9f90-7deb00041918)
 Call ID: 93429e6d-044e-4c34-9f90-7deb00041918
  Args:
    source: Princess_Elisabeth_Sybille_of_Saxe_Weimar_Eisenach
    type: :Person
  AddLiteral (250d1fd5-25c0-4c00-895c-edccbd27b695)
 Call ID: 250d1fd5-25c0-4c00-895c-edccbd27b695
  Args:
    source: Duke_John_Albert_of_Mecklenburg
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1886
  AssignClass (e93e713a-60eb-4a43-87a2-245c7b951099)
 Call ID: e93e713a-60eb-4a43-87a2-245c7b951099
  Args:
    type: :Woman
    source: Princess_Elisabeth_of_Stolberg_Rossla
  AssignClass (852c69a1-7bae-4f5b-8e5f-389150308f5d)
 Call ID: 852c69a1-7bae-4f5b-8e5f-389150308f5d
  Args:
    type: :Person
    source: Princess_Elisabeth_of_Stolberg_Rossla
  AddLiteral (ed087df8-cc62-498a-a1d8-f94747e5d539)
 Call ID: ed087df8-cc62-498a-a1d8-f94747e5d539
  Args:
    source: Duke_John_Albert_of_Mecklenburg
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1909
  AssignClass (e3469b77-4395-467a-a510-6141c8a0a2b2)
 Call ID: e3469b77-4395-467a-a510-6141c8a0a2b2
  Args:
    source: Duke_Adolf_Friedrich
    type: :Man
  AssignClass (4a0726a0-74d7-43ac-be16-4271adce0385)
 Call ID: 4a0726a0-74d7-43ac-be16-4271adce0385
  Args:
    type: :Person
    source: Duke_Adolf_Friedrich
  Finish (90e9ef85-5a72-435a-9caa-12fbf854bd68)
 Call ID: 90e9ef85-5a72-435a-9caa-12fbf854bd68
  Args: