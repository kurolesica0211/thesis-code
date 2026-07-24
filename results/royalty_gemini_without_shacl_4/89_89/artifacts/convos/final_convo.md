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
Prince Nicholas of Greece and Denmark (Greek: Νικόλαος, romanized: Nikólaos; 22 January 1872 – 8 February 1938) was the fourth child and third son of King George I of Greece, and of Queen Olga.
He was known as "Greek Nicky" within the family to distinguish him from his cousin Emperor Nicholas II of Russia (first cousin on the paternal side and second cousin on the maternal side).
Prince Nicholas was a talented painter, often signing his works as "Nicolas Leprince".
Marriage and issue

He married Grand Duchess Elena Vladimirovna of Russia (1882–1957), daughter of Grand Duke Vladimir Alexandrovich of Russia and Marie of Mecklenburg-Schwerin, the only sister of the future Russian imperial pretender, Grand Duke Kirill Vladimirovich, and his second cousin through his mother Olga Constantinovna of Russia and her father Grand Duke Vladimir Alexandrovich of Russia, on 29 August 1902 in Tsarskoye Selo, Russia.
Residence in Athens

Nicholas' marriage significantly improved his own financial position; his wife Elena received the customary imperial dowry of a Russian Grand Duchess, amounting to 1,000,000 roubles.
The dowry capital was held in Russia, from which Elena was paid an annual income of 50,000 roubles.
After their marriage the couple resided in Athens; in late 1902 they purchased a large house near the city centre, which was thereafter known as the Nicholas Palace.
Prince and Princess Nicholas took up residence at the newly-renovated Nicholas Palace in 1904.
The advent of the Russian Revolution in 1917 and the exile of the Greek Royal Family in 1923 had a significant impact on the couple's income, and as a result the Nicholas Palace was leased to the Hotel Grande Bretagne during the 1920s, who used the building as a 60-bed luxury annex known as the “Petit Palais”.
The Italian Government later purchased the Nicholas Palace from the widowed Princess Nicholas in 1955; the site has subsequently remained the home of the Italian Embassy in Athens ever since.
Public life

Along with his elder brothers Constantine and George, Nicholas helped to organize the 1896 Summer Olympics in Athens, the first to be held since 393.
Nicholas served as president of the Sub-Committee for Shooting.
His father bequeathed him the Royal Theater of Greece which Nicholas, in turn, transferred to the Greek state in 1935.
He was friends with George Simitis and was godfather to his son, future socialist Prime Minister Kostas Simitis.
Death and burial

Prince Nicholas died in Athens on February 8, 1938 and was buried in the Royal tomb at the Palace of Tatoi.



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
  AssignClass (7006a1c8-3077-48cd-af96-86021e07c45a)
 Call ID: 7006a1c8-3077-48cd-af96-86021e07c45a
  Args:
    type: :Man
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (e6f35284-e357-4002-b3db-225c4c7ab9e0)
 Call ID: e6f35284-e357-4002-b3db-225c4c7ab9e0
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (d8f2083c-8580-431b-be8f-d9b94f6688d6)
 Call ID: d8f2083c-8580-431b-be8f-d9b94f6688d6
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_value: 1872
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (b0020bc8-254d-4a02-8daf-32f10e2229f8)
 Call ID: b0020bc8-254d-4a02-8daf-32f10e2229f8
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_value: 1938
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddLiteral (a8dd10aa-702f-4a10-bec2-ac2ace9abc03)
 Call ID: a8dd10aa-702f-4a10-bec2-ac2ace9abc03
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Greek Nicky
  AddLiteral (063675ba-d685-4c22-a934-85a3e8c4e79b)
 Call ID: 063675ba-d685-4c22-a934-85a3e8c4e79b
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_value: Nicolas Leprince
    literal_type: xsd:string
    relation: :alsoKnownAs
  AssignClass (09f5b7f6-3bf0-4beb-82e7-421eb65fbba8)
 Call ID: 09f5b7f6-3bf0-4beb-82e7-421eb65fbba8
  Args:
    type: :Man
    source: King_George_I_of_Greece
  AssignClass (b86dd08d-b08f-4aea-b1ff-d01170fb98ec)
 Call ID: b86dd08d-b08f-4aea-b1ff-d01170fb98ec
  Args:
    type: :Person
    source: King_George_I_of_Greece
  AssignClass (7a9cbb8c-fc82-4818-99fd-622afaeaac2b)
 Call ID: 7a9cbb8c-fc82-4818-99fd-622afaeaac2b
  Args:
    type: :Woman
    source: Queen_Olga
  AssignClass (6e161398-9930-4044-9e39-9686aedebb1d)
 Call ID: 6e161398-9930-4044-9e39-9686aedebb1d
  Args:
    type: :Person
    source: Queen_Olga
  AddTriple (66f3ba16-b16a-4cc9-8980-d2e6cf9121f8)
 Call ID: 66f3ba16-b16a-4cc9-8980-d2e6cf9121f8
  Args:
    relation: :hasFather
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: King_George_I_of_Greece
  AddTriple (ea5195b2-f8e3-42f0-af97-21871613b239)
 Call ID: ea5195b2-f8e3-42f0-af97-21871613b239
  Args:
    relation: :hasMother
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: Queen_Olga
  AssignClass (c379dd62-6a02-4529-8e9f-c2e1a3e6dcab)
 Call ID: c379dd62-6a02-4529-8e9f-c2e1a3e6dcab
  Args:
    type: :Woman
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (1367b8e9-5fd0-4ed6-af33-437929f78c55)
 Call ID: 1367b8e9-5fd0-4ed6-af33-437929f78c55
  Args:
    type: :Person
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddLiteral (b200f725-d7be-42d1-8ffe-fff33f89f01d)
 Call ID: b200f725-d7be-42d1-8ffe-fff33f89f01d
  Args:
    literal_value: 1882
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AddLiteral (41ce5da9-5d99-44f3-b566-019ffc068538)
 Call ID: 41ce5da9-5d99-44f3-b566-019ffc068538
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1957
  AddLiteral (0d59e67b-50a2-4375-9a21-4db02f83d589)
 Call ID: 0d59e67b-50a2-4375-9a21-4db02f83d589
  Args:
    literal_value: 1902
    relation: :hasMarriageYear
    literal_type: xsd:integer
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (6319488e-2ba8-4d48-9712-643ee5bc9697)
 Call ID: 6319488e-2ba8-4d48-9712-643ee5bc9697
  Args:
    type: :Man
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AssignClass (ed71fb42-bc0b-4063-80f2-bdacc3bb9c23)
 Call ID: ed71fb42-bc0b-4063-80f2-bdacc3bb9c23
  Args:
    type: :Person
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AssignClass (1e975df5-fc11-482a-a1fe-b3891b717a96)
 Call ID: 1e975df5-fc11-482a-a1fe-b3891b717a96
  Args:
    type: :Woman
    source: Marie_of_Mecklenburg-Schwerin
  AssignClass (37415cf3-e271-40c8-853c-df0832873741)
 Call ID: 37415cf3-e271-40c8-853c-df0832873741
  Args:
    type: :Person
    source: Marie_of_Mecklenburg-Schwerin
  AddTriple (3307fa9a-c620-4855-8cdc-b96eafa30ba4)
 Call ID: 3307fa9a-c620-4855-8cdc-b96eafa30ba4
  Args:
    relation: :hasFather
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    target: Grand_Duke_Vladimir_Alexandrovich_of_Russia
  AddTriple (c7555665-a468-40a2-83d0-7b17f0d4adb8)
 Call ID: c7555665-a468-40a2-83d0-7b17f0d4adb8
  Args:
    relation: :hasMother
    target: Marie_of_Mecklenburg-Schwerin
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (717e0e8d-c801-4117-a6fd-97595c9a855d)
 Call ID: 717e0e8d-c801-4117-a6fd-97595c9a855d
  Args:
    type: :Man
    source: Grand_Duke_Kirill_Vladimirovich
  AssignClass (2cfdd7f4-4fdb-4bbe-a52a-ef95124c7b88)
 Call ID: 2cfdd7f4-4fdb-4bbe-a52a-ef95124c7b88
  Args:
    type: :Person
    source: Grand_Duke_Kirill_Vladimirovich
  AddTriple (dcbbc279-33b8-4a81-b1ae-c88a2ef120da)
 Call ID: dcbbc279-33b8-4a81-b1ae-c88a2ef120da
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    target: Grand_Duke_Kirill_Vladimirovich
    relation: :isSiblingOf
  AssignClass (0032bb0d-2421-4bbc-a0a1-80f389738d33)
 Call ID: 0032bb0d-2421-4bbc-a0a1-80f389738d33
  Args:
    type: :Man
    source: Constantine
  AssignClass (dc9156f0-605c-43c7-8130-e9947c877de8)
 Call ID: dc9156f0-605c-43c7-8130-e9947c877de8
  Args:
    type: :Person
    source: Constantine
  AssignClass (7f1e00eb-cff3-4549-a56f-8beae8acf699)
 Call ID: 7f1e00eb-cff3-4549-a56f-8beae8acf699
  Args:
    type: :Man
    source: George
  AssignClass (308af732-71b1-4538-b7f3-bce8f5d905be)
 Call ID: 308af732-71b1-4538-b7f3-bce8f5d905be
  Args:
    type: :Person
    source: George
  AddTriple (c8794fb2-d63c-456a-8a90-663190be20c8)
 Call ID: c8794fb2-d63c-456a-8a90-663190be20c8
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: Constantine
    relation: :isSiblingOf
  AddTriple (f99e8d22-0e52-46f8-8844-e77f34e47f97)
 Call ID: f99e8d22-0e52-46f8-8844-e77f34e47f97
  Args:
    target: George
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :isSiblingOf
  AssignClass (35566f91-4d60-4ab7-a1b5-b49d61dbe683)
 Call ID: 35566f91-4d60-4ab7-a1b5-b49d61dbe683
  Args:
    type: :Man
    source: George_Simitis
  AssignClass (5945e223-dce1-441a-b36b-ba7c55940add)
 Call ID: 5945e223-dce1-441a-b36b-ba7c55940add
  Args:
    type: :Person
    source: George_Simitis
  AssignClass (1109ed74-5935-4704-95af-85b503e21933)
 Call ID: 1109ed74-5935-4704-95af-85b503e21933
  Args:
    type: :Man
    source: Kostas_Simitis
  AssignClass (1f7f23b0-d3d1-44c2-adb5-7f34fc3d5a43)
 Call ID: 1f7f23b0-d3d1-44c2-adb5-7f34fc3d5a43
  Args:
    type: :Person
    source: Kostas_Simitis
  AddTriple (e0492f05-e312-42fa-83a3-237fb0883518)
 Call ID: e0492f05-e312-42fa-83a3-237fb0883518
  Args:
    relation: :hasFather
    source: Kostas_Simitis
    target: George_Simitis
  Finish (75f61a53-d9dd-464f-a0c0-bb579deccf9b)
 Call ID: 75f61a53-d9dd-464f-a0c0-bb579deccf9b
  Args: