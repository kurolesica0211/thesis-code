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
Prince Heinrich of Prussia (German: Albert Wilhelm Heinrich; 14 August 1862 – 20 April 1929) was a younger brother of German Emperor and King of Prussia Wilhelm II and a Prince of Prussia.
Biography

Born in Berlin, Prince Heinrich was the third child and second son of eight children born to Crown Prince Frederick William (later Emperor Frederick III), and Victoria, Princess Royal (later Empress Victoria and in widowhood Empress Frederick), eldest daughter of the British Queen Victoria.
Henry was three years younger than his brother, the future Emperor William II (born 27 January 1859).
He was born on the same day as King Frederick William I "Soldier-King" of Prussia.
Early commands

As a Prussian prince, Henry quickly achieved command.
Squadron commands

From 1897, Prince Henry commanded several naval task forces; these included an improvised squadron that took part with the East Asia Squadron in consolidating and securing the German hold on the region of Kiaochow and the port of Tsingtao in 1898.
The prince's success was more of the diplomatic than the military variety; he became the first European potentate ever to be received at the Chinese imperial court.
From 1906 to 1909, Henry was commander of the High Seas Fleet.
I

At the beginning of World War I, Prince Henry was named as Commander-in-Chief of the Baltic Fleet.
After the end of hostilities with Russia, his mission was ended, and Prince Henry simply left active duty.
With the war's end and the dissolution of the monarchy in Germany, Prince Henry left the navy.
Family

On 24 May 1888, Henry married Princess Irene of Hesse and by Rhine, his first cousin.
His dying father, German Emperor Frederick III and his mother Empress Victoria were in attendance.
The marriage produced three children:


Their sons Waldemar and Heinrich were both hemophiliacs, a disease which they inherited through Irene from the maternal grandmother of both of their parents, Queen Victoria, who was a carrier.
Personality and private life

Henry received one of the first pilot's licenses in Germany, and was judged a spirited and excellent seaman.
A yachting enthusiast, Prince Henry became one of the first members of the Yacht Club of Kiel, established by a group of naval officers in 1887, and quickly became the club's patron.
Henry was interested in motor cars as well and supposedly invented a windshield wiper and, according to other sources, the car horn.
In his honor, the Prinz-Heinrich-Fahrt (Prince Heinrich Tour) was established in 1908, like the earlier Kaiserpreis a precursor to the German Grand Prix.
Henry and his brother William gave patronage to the Kaiserlicher Automobilclub (Imperial Automobile Club).
From 1911 to 1914 the British car makers Vauxhall Motors produced a model, the C-10, which was called the "Vauxhall Prince Henry" in his honour after initially being built for participation in the 1911 race.
After the German Revolution, Henry lived with his family in Hemmelmark near Eckernförde, in Schleswig-Holstein.
He popularized the Prince Henry cap, which is still worn, especially by older sailors.
In 1899, Henry received an honorary doctorate (Doctor of Engineering honoris causa) from the Technische Hochschule in Charlottenburg (now Technische Universität Berlin) .
Prince Henry died of throat cancer on 20 April 1929 in Hemmelmark.



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
  AssignClass (14b8c562-979d-48e7-b455-76553164f60b)
 Call ID: 14b8c562-979d-48e7-b455-76553164f60b
  Args:
    type: :Man
    source: Prince_Heinrich_of_Prussia
  AssignClass (2ccba342-7d71-4d29-a0b1-0cb23e4325d4)
 Call ID: 2ccba342-7d71-4d29-a0b1-0cb23e4325d4
  Args:
    source: Prince_Heinrich_of_Prussia
    type: :Person
  AddLiteral (2e543005-0b46-42d8-8f83-0981cf828dc2)
 Call ID: 2e543005-0b46-42d8-8f83-0981cf828dc2
  Args:
    literal_value: 1862
    literal_type: xsd:integer
    source: Prince_Heinrich_of_Prussia
    relation: :hasBirthYear
  AddLiteral (6aa9abf0-87b8-42e8-9ccb-ce85b50cf6e7)
 Call ID: 6aa9abf0-87b8-42e8-9ccb-ce85b50cf6e7
  Args:
    literal_type: xsd:integer
    literal_value: 1929
    relation: :hasDeathYear
    source: Prince_Heinrich_of_Prussia
  AssignClass (32d5d1a7-7ce2-4c34-bdef-b203f5d4c74f)
 Call ID: 32d5d1a7-7ce2-4c34-bdef-b203f5d4c74f
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (bcffebe8-e986-43a1-8d7d-37eb5ff69b35)
 Call ID: bcffebe8-e986-43a1-8d7d-37eb5ff69b35
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (9f456c2c-fd8d-41ba-aeca-d8d96a9fb38a)
 Call ID: 9f456c2c-fd8d-41ba-aeca-d8d96a9fb38a
  Args:
    source: Prince_Heinrich_of_Prussia
    relation: :isBrotherOf
    target: Wilhelm_II
  AssignClass (abd4117d-ad19-425e-a78e-df608f74538a)
 Call ID: abd4117d-ad19-425e-a78e-df608f74538a
  Args:
    source: Frederick_III
    type: :Man
  AssignClass (2a9e62d6-b82c-4315-9cb0-e62a04e98c1d)
 Call ID: 2a9e62d6-b82c-4315-9cb0-e62a04e98c1d
  Args:
    source: Frederick_III
    type: :Person
  AssignClass (357b3ea0-4c7f-4397-a96a-9285e1233e6b)
 Call ID: 357b3ea0-4c7f-4397-a96a-9285e1233e6b
  Args:
    source: Victoria_Princess_Royal
    type: :Woman
  AssignClass (9434cf55-869d-488a-8aa1-5a2423afb080)
 Call ID: 9434cf55-869d-488a-8aa1-5a2423afb080
  Args:
    type: :Person
    source: Victoria_Princess_Royal
  AddTriple (d1cc1036-9344-40f5-8d58-1292272fc466)
 Call ID: d1cc1036-9344-40f5-8d58-1292272fc466
  Args:
    target: Frederick_III
    relation: :hasFather
    source: Prince_Heinrich_of_Prussia
  AddTriple (eb1a1217-443a-4be0-9174-162e1bb2bb3a)
 Call ID: eb1a1217-443a-4be0-9174-162e1bb2bb3a
  Args:
    target: Victoria_Princess_Royal
    relation: :hasMother
    source: Prince_Heinrich_of_Prussia
  AssignClass (4945c18d-6ca7-4b25-87f8-79b626adde7c)
 Call ID: 4945c18d-6ca7-4b25-87f8-79b626adde7c
  Args:
    type: :Woman
    source: Queen_Victoria
  AssignClass (a3453f0c-854b-4d2e-8ae4-18912d6c7865)
 Call ID: a3453f0c-854b-4d2e-8ae4-18912d6c7865
  Args:
    type: :Person
    source: Queen_Victoria
  AddTriple (0119568e-c0c8-400d-bac1-c96b2635fedc)
 Call ID: 0119568e-c0c8-400d-bac1-c96b2635fedc
  Args:
    source: Victoria_Princess_Royal
    relation: :hasMother
    target: Queen_Victoria
  AssignClass (8a00ac47-a995-456c-b8d7-73ef4769ed19)
 Call ID: 8a00ac47-a995-456c-b8d7-73ef4769ed19
  Args:
    source: Princess_Irene_of_Hesse
    type: :Woman
  AssignClass (ab1c4dd7-fe05-4cd7-b603-bcbb3754cdcc)
 Call ID: ab1c4dd7-fe05-4cd7-b603-bcbb3754cdcc
  Args:
    type: :Person
    source: Princess_Irene_of_Hesse
  AddLiteral (c39e1e39-f0e3-4937-923c-4152fb7eab63)
 Call ID: c39e1e39-f0e3-4937-923c-4152fb7eab63
  Args:
    source: Prince_Heinrich_of_Prussia
    relation: :hasMarriageYear
    literal_value: 1888
    literal_type: xsd:integer
  AddTriple (d2357e83-5357-4032-8caf-197e03cacd49)
 Call ID: d2357e83-5357-4032-8caf-197e03cacd49
  Args:
    relation: :hasRelation
    source: Prince_Heinrich_of_Prussia
    target: Princess_Irene_of_Hesse
  AssignClass (4e79433c-d771-4c0e-a2ab-b9eecf04a378)
 Call ID: 4e79433c-d771-4c0e-a2ab-b9eecf04a378
  Args:
    type: :Man
    source: Waldemar
  AssignClass (11e927cb-e98a-4466-9d47-153cbc102797)
 Call ID: 11e927cb-e98a-4466-9d47-153cbc102797
  Args:
    type: :Person
    source: Waldemar
  AssignClass (50c10550-1fb6-435a-b0c9-4b585d72c1af)
 Call ID: 50c10550-1fb6-435a-b0c9-4b585d72c1af
  Args:
    source: Heinrich_son
    type: :Man
  AssignClass (db98a863-a248-4c54-aa7c-4bba0e225d96)
 Call ID: db98a863-a248-4c54-aa7c-4bba0e225d96
  Args:
    source: Heinrich_son
    type: :Person
  AddTriple (401bd541-4b2e-4870-9183-9c621e343d2b)
 Call ID: 401bd541-4b2e-4870-9183-9c621e343d2b
  Args:
    target: Waldemar
    source: Prince_Heinrich_of_Prussia
    relation: :hasChild
  AddTriple (9cb4a866-ab2f-46e1-8261-4d448bd2a471)
 Call ID: 9cb4a866-ab2f-46e1-8261-4d448bd2a471
  Args:
    target: Heinrich_son
    source: Prince_Heinrich_of_Prussia
    relation: :hasChild
  AddTriple (d21a036d-10f7-48a9-b01a-4b3174e23164)
 Call ID: d21a036d-10f7-48a9-b01a-4b3174e23164
  Args:
    target: Waldemar
    source: Princess_Irene_of_Hesse
    relation: :hasChild
  AddTriple (47feef92-75f9-462b-920e-e941402101df)
 Call ID: 47feef92-75f9-462b-920e-e941402101df
  Args:
    relation: :hasChild
    source: Princess_Irene_of_Hesse
    target: Heinrich_son
  Finish (8fdaf7b5-bb15-41e4-998b-03ff903c2562)
 Call ID: 8fdaf7b5-bb15-41e4-998b-03ff903c2562
  Args: