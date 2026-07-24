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
Princess Alexandra of Greece and Denmark (Greek: Αλεξάνδρα; romanized: Alexándra), later known as Grand Duchess Alexandra Georgievna of Russia (Russian: Алекса́ндра Гео́ргиевна); 30 August  1870 – 24 September  1891), was a member of the Greek royal family by birth and of the Russian imperial family by marriage.
Alexandra was the daughter of George I of Greece and Olga Constantinovna of Russia, and grew up in Athens.
In 1889, she married Grand Duke Paul Alexandrovich of Russia, her first cousin once removed.
The couple settled in Saint Petersburg and they had two children: Grand Duchess Maria Pavlovna (1890–1958) and Grand Duke Dmitri Pavlovich (1891–1942).
Early life

Princess Alexandra of Greece and Denmark was born on 30 August  1870 at Mon Repos, the summer residence of the Greek royal family on the island of Corfu.
She was the third child and eldest daughter of King George I of Greece and his wife, Grand Duchess Olga Constantinovna of Russia.
Alexandra's father was not a native Greek, but he had been born a Danish prince named Christian Wilhelm of Schleswig-Holstein-Sonderburg-Glücksburg, a son of Christian IX, King of Denmark, and he had been elected to the Greek throne at the age of seventeen.
Five of his sons (Constantine, George, Nicholas, Andrew and Christopher), and two daughters (Alexandra and Maria), attained adulthood.
King George was a taciturn man, but contrary to the general approach of the time, he believed in happy rambunctious children.
The long corridors of the royal palace in Athens were used by Alexandra and her siblings for all types of play and sometimes a "bike ride" would be led by the King himself.
Alexandra, nicknamed "Aline" within her family, or Greek Alix, to distinguish her from her aunt and godmother, Alexandra, Princess of Wales, had a sunny disposition and was much loved by her family.
"


Alexandra's playmates were her brother Nicholas and her sister Maria, who followed her in age.
Alexandra spent many holidays in Denmark visiting her paternal grandparents.
In Denmark, Alexandra and her siblings met their Russian and British cousins in large family gatherings.
Marriage and children

When she was 18 years old, she was married to Grand Duke Paul Alexandrovich of Russia, her maternal first cousin once removed and the youngest child and sixth son of Emperor Alexander II and his first wife, Princess Marie of Hesse and by Rhine.
They had become close when Grand Duke Paul spent winters in Greece due to his frequent respiratory illnesses.
The Greek royal family also frequently spent holidays with the Romanov family on visits to Russia or Denmark.
They had two children:


Death

Seven months into her second pregnancy, Alexandra took a walk with her friends on the bank of the Moskva River and jumped directly into a boat that was permanently moored there, but fell as she got in.
The Grand Duchess was buried in the Peter and Paul Cathedral, St. Petersburg.
Her husband later morganatically remarried Olga Karnovich.
Alexandra's son would be involved in the murder of Grigori Rasputin, a friend of Tsarina Alexandra Feodorovna, in 1916.
In 1939 during the reign of her nephew George II of Greece, the Greek government obtained permission from the Soviet government under Joseph Stalin to rebury Princess Alexandra in Greece.
Alexandra's marble tombstone over an empty tomb is still in its place in the Peter and Paul Cathedral.
The "Alexandra Maternity Hospital" (now "Alexandra General Hospital") in Athens was later named in her memory by another nephew, King Paul; it was affiliated with the University of Athens with a special remit to research and combat postpartum maternal mortality.



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
  AssignClass (99b20b24-0c02-4f3b-bd26-f4d64bd5dcc2)
 Call ID: 99b20b24-0c02-4f3b-bd26-f4d64bd5dcc2
  Args:
    source: Princess_Alexandra_of_Greece_and_Denmark
    type: :Woman
  AssignClass (f9673288-5b57-4840-ab91-df08652f63e2)
 Call ID: f9673288-5b57-4840-ab91-df08652f63e2
  Args:
    source: Princess_Alexandra_of_Greece_and_Denmark
    type: :Person
  AddLiteral (00a41e0c-a322-4b13-b540-92117fe6dd39)
 Call ID: 00a41e0c-a322-4b13-b540-92117fe6dd39
  Args:
    literal_value: Grand Duchess Alexandra Georgievna of Russia
    source: Princess_Alexandra_of_Greece_and_Denmark
    literal_type: xsd:string
    relation: :alsoKnownAs
  AddLiteral (271e0e24-757a-4610-9d57-4c199542611e)
 Call ID: 271e0e24-757a-4610-9d57-4c199542611e
  Args:
    literal_value: 1870
    source: Princess_Alexandra_of_Greece_and_Denmark
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (6aa763bb-183f-4864-9ec8-f34b2cdf0e56)
 Call ID: 6aa763bb-183f-4864-9ec8-f34b2cdf0e56
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1891
    source: Princess_Alexandra_of_Greece_and_Denmark
  AssignClass (083c9fbe-fd95-4409-af7f-630eb456efdc)
 Call ID: 083c9fbe-fd95-4409-af7f-630eb456efdc
  Args:
    source: George_I_of_Greece
    type: :Man
  AssignClass (24492fff-fc5c-4946-b9a9-a003b899d62c)
 Call ID: 24492fff-fc5c-4946-b9a9-a003b899d62c
  Args:
    type: :Person
    source: George_I_of_Greece
  AssignClass (04aac610-7184-4e33-9227-2a353743068b)
 Call ID: 04aac610-7184-4e33-9227-2a353743068b
  Args:
    type: :Woman
    source: Olga_Constantinovna_of_Russia
  AssignClass (17240d65-94be-4d66-9866-e435376ba642)
 Call ID: 17240d65-94be-4d66-9866-e435376ba642
  Args:
    type: :Person
    source: Olga_Constantinovna_of_Russia
  AddTriple (7ff54e68-1b6a-48dc-b130-568ad600ab2a)
 Call ID: 7ff54e68-1b6a-48dc-b130-568ad600ab2a
  Args:
    relation: :hasFather
    source: Princess_Alexandra_of_Greece_and_Denmark
    target: George_I_of_Greece
  AddTriple (91035781-3d8f-417c-a4fc-195c66456e82)
 Call ID: 91035781-3d8f-417c-a4fc-195c66456e82
  Args:
    relation: :hasMother
    source: Princess_Alexandra_of_Greece_and_Denmark
    target: Olga_Constantinovna_of_Russia
  AssignClass (07ac10f1-524f-451d-9fe0-c0e5462f7d86)
 Call ID: 07ac10f1-524f-451d-9fe0-c0e5462f7d86
  Args:
    type: :Man
    source: Grand_Duke_Paul_Alexandrovich_of_Russia
  AssignClass (bd47fccc-f962-4dc1-bed1-7727760cdb6d)
 Call ID: bd47fccc-f962-4dc1-bed1-7727760cdb6d
  Args:
    source: Grand_Duke_Paul_Alexandrovich_of_Russia
    type: :Person
  AddTriple (3865f810-b020-4355-be6f-df69859d8b91)
 Call ID: 3865f810-b020-4355-be6f-df69859d8b91
  Args:
    source: Princess_Alexandra_of_Greece_and_Denmark
    target: Grand_Duke_Paul_Alexandrovich_of_Russia
    relation: :hasRelation
  AddLiteral (2b0963ea-5718-4ade-8e12-d70a1961e8f2)
 Call ID: 2b0963ea-5718-4ade-8e12-d70a1961e8f2
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1889
    source: Princess_Alexandra_of_Greece_and_Denmark
  AssignClass (cf7f4611-5474-458b-94e0-18a178c097f8)
 Call ID: cf7f4611-5474-458b-94e0-18a178c097f8
  Args:
    source: Maria_Pavlovna
    type: :Woman
  AssignClass (274be93b-1e78-4d65-9a5b-7c3b486c1296)
 Call ID: 274be93b-1e78-4d65-9a5b-7c3b486c1296
  Args:
    source: Maria_Pavlovna
    type: :Person
  AssignClass (4bfd61bc-33d5-4f42-bf73-48369bbcd155)
 Call ID: 4bfd61bc-33d5-4f42-bf73-48369bbcd155
  Args:
    type: :Man
    source: Dmitri_Pavlovich
  AssignClass (c85fdd02-4d8b-4279-bc8f-aca5010e5cbe)
 Call ID: c85fdd02-4d8b-4279-bc8f-aca5010e5cbe
  Args:
    source: Dmitri_Pavlovich
    type: :Person
  AddTriple (93b26c28-b04d-4fff-9f0e-2899ff11900b)
 Call ID: 93b26c28-b04d-4fff-9f0e-2899ff11900b
  Args:
    relation: :hasChild
    source: Princess_Alexandra_of_Greece_and_Denmark
    target: Maria_Pavlovna
  AddTriple (f6c15b65-e750-4d9f-9266-13292ad574b6)
 Call ID: f6c15b65-e750-4d9f-9266-13292ad574b6
  Args:
    relation: :hasChild
    source: Princess_Alexandra_of_Greece_and_Denmark
    target: Dmitri_Pavlovich
  AddTriple (3574e072-2ad6-4447-952c-9c05f3e75ebb)
 Call ID: 3574e072-2ad6-4447-952c-9c05f3e75ebb
  Args:
    source: Grand_Duke_Paul_Alexandrovich_of_Russia
    target: Maria_Pavlovna
    relation: :hasChild
  AddTriple (e5183108-1fd6-4a20-9849-29284306b69e)
 Call ID: e5183108-1fd6-4a20-9849-29284306b69e
  Args:
    source: Grand_Duke_Paul_Alexandrovich_of_Russia
    target: Dmitri_Pavlovich
    relation: :hasChild
  AssignClass (efca0eae-0dad-448b-9daf-9cd636ca2965)
 Call ID: efca0eae-0dad-448b-9daf-9cd636ca2965
  Args:
    type: :Man
    source: Christian_IX_of_Denmark
  AssignClass (edbdedb1-dc10-4aa2-9844-5ab955c1f1df)
 Call ID: edbdedb1-dc10-4aa2-9844-5ab955c1f1df
  Args:
    type: :Person
    source: Christian_IX_of_Denmark
  AddTriple (26449487-2c34-4706-85b4-99095cc03e36)
 Call ID: 26449487-2c34-4706-85b4-99095cc03e36
  Args:
    target: Christian_IX_of_Denmark
    source: George_I_of_Greece
    relation: :hasFather
  AssignClass (2033064d-1913-4716-bdaf-c75440ca1217)
 Call ID: 2033064d-1913-4716-bdaf-c75440ca1217
  Args:
    type: :Man
    source: Nicholas_of_Greece
  AssignClass (5e5a2f7d-9dc1-41c7-9854-0988955320a2)
 Call ID: 5e5a2f7d-9dc1-41c7-9854-0988955320a2
  Args:
    source: Nicholas_of_Greece
    type: :Person
  AssignClass (8f225fd8-a412-47d0-98f4-ec128f22aae7)
 Call ID: 8f225fd8-a412-47d0-98f4-ec128f22aae7
  Args:
    type: :Woman
    source: Maria_of_Greece
  AssignClass (bbff9368-4905-4e8d-9ee3-f7412a83d5cf)
 Call ID: bbff9368-4905-4e8d-9ee3-f7412a83d5cf
  Args:
    source: Maria_of_Greece
    type: :Person
  AddTriple (e6c9787a-d875-46c9-82e9-309215e69eec)
 Call ID: e6c9787a-d875-46c9-82e9-309215e69eec
  Args:
    relation: :isSiblingOf
    source: Princess_Alexandra_of_Greece_and_Denmark
    target: Nicholas_of_Greece
  AddTriple (c0d60017-b377-48e0-81cc-7586c6f4abee)
 Call ID: c0d60017-b377-48e0-81cc-7586c6f4abee
  Args:
    relation: :isSiblingOf
    source: Princess_Alexandra_of_Greece_and_Denmark
    target: Maria_of_Greece
  AssignClass (eda1e259-763d-411a-9c20-e27296dde1a1)
 Call ID: eda1e259-763d-411a-9c20-e27296dde1a1
  Args:
    type: :Man
    source: Alexander_II_of_Russia
  AssignClass (80c03991-b800-408f-8fed-c7a584c98aad)
 Call ID: 80c03991-b800-408f-8fed-c7a584c98aad
  Args:
    source: Alexander_II_of_Russia
    type: :Person
  AssignClass (c724007d-cd7e-4497-9973-d21a34e369cc)
 Call ID: c724007d-cd7e-4497-9973-d21a34e369cc
  Args:
    type: :Woman
    source: Marie_of_Hesse_and_by_Rhine
  AssignClass (ddf529e6-9953-4dae-ac83-a8d56abec713)
 Call ID: ddf529e6-9953-4dae-ac83-a8d56abec713
  Args:
    source: Marie_of_Hesse_and_by_Rhine
    type: :Person
  AddTriple (733e7b4a-6e66-4d40-a735-77174f6db386)
 Call ID: 733e7b4a-6e66-4d40-a735-77174f6db386
  Args:
    target: Alexander_II_of_Russia
    source: Grand_Duke_Paul_Alexandrovich_of_Russia
    relation: :hasFather
  AddTriple (dd68608a-1333-44b6-acfa-63f06fbfed6e)
 Call ID: dd68608a-1333-44b6-acfa-63f06fbfed6e
  Args:
    relation: :hasMother
    source: Grand_Duke_Paul_Alexandrovich_of_Russia
    target: Marie_of_Hesse_and_by_Rhine
  Finish (b5f24a82-dfca-40cb-abb2-30ce15cb4785)
 Call ID: b5f24a82-dfca-40cb-abb2-30ce15cb4785
  Args: