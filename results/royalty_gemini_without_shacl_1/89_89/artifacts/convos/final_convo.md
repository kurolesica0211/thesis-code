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
  AssignClass (44e45de8-cd6c-4dba-80fa-7b2adc04b854)
 Call ID: 44e45de8-cd6c-4dba-80fa-7b2adc04b854
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    type: :Man
  AssignClass (1d189644-645e-447b-9fd5-e096639c2eab)
 Call ID: 1d189644-645e-447b-9fd5-e096639c2eab
  Args:
    type: :Person
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (7d570809-143c-41d5-bafa-fc5bdbda4860)
 Call ID: 7d570809-143c-41d5-bafa-fc5bdbda4860
  Args:
    literal_value: 1872
    relation: :hasBirthYear
    source: Prince_Nicholas_of_Greece_and_Denmark
    literal_type: xsd:integer
  AddLiteral (a2440d45-f09a-4fcf-b695-98d23c9734ea)
 Call ID: a2440d45-f09a-4fcf-b695-98d23c9734ea
  Args:
    literal_value: 1938
    literal_type: xsd:integer
    relation: :hasDeathYear
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddLiteral (c4d85187-4dc7-473e-8d98-1a8d992cc177)
 Call ID: c4d85187-4dc7-473e-8d98-1a8d992cc177
  Args:
    literal_value: Greek Nicky
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :knownAs
    literal_type: xsd:string
  AddLiteral (130d6f6f-992a-4a28-85a2-80dc0a4e2ac3)
 Call ID: 130d6f6f-992a-4a28-85a2-80dc0a4e2ac3
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :knownAs
    literal_type: xsd:string
    literal_value: Nicolas Leprince
  AssignClass (886a422c-e8be-4a5b-8c01-62b7497ae8e7)
 Call ID: 886a422c-e8be-4a5b-8c01-62b7497ae8e7
  Args:
    source: King_George_I_of_Greece
    type: :Man
  AssignClass (a4178e94-8acf-4b03-9b5e-555f0795dde2)
 Call ID: a4178e94-8acf-4b03-9b5e-555f0795dde2
  Args:
    source: King_George_I_of_Greece
    type: :Person
  AssignClass (275a52f6-5d3a-4110-b5f0-87a591424b11)
 Call ID: 275a52f6-5d3a-4110-b5f0-87a591424b11
  Args:
    type: :Woman
    source: Queen_Olga
  AssignClass (fde60945-c30f-4980-81cb-673581dc0506)
 Call ID: fde60945-c30f-4980-81cb-673581dc0506
  Args:
    type: :Person
    source: Queen_Olga
  AddTriple (addc4868-9e12-4783-bf2b-e29ea6dcc01f)
 Call ID: addc4868-9e12-4783-bf2b-e29ea6dcc01f
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasFather
    target: King_George_I_of_Greece
  AddTriple (168e28c3-4122-4b87-99c1-071f3cfb8617)
 Call ID: 168e28c3-4122-4b87-99c1-071f3cfb8617
  Args:
    target: Queen_Olga
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasMother
  AssignClass (8f704874-92ef-4e71-a493-899daa140f23)
 Call ID: 8f704874-92ef-4e71-a493-899daa140f23
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Woman
  AssignClass (a151753e-eb85-433a-b1bb-a7c84bf1240d)
 Call ID: a151753e-eb85-433a-b1bb-a7c84bf1240d
  Args:
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    type: :Person
  AddLiteral (71527cc5-8c5a-44b0-8545-c2f08d5460fa)
 Call ID: 71527cc5-8c5a-44b0-8545-c2f08d5460fa
  Args:
    source: Prince_Nicholas_of_Greece_and_Denmark
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1902
  AddTriple (e579559c-4e14-45dc-8e41-7ce463813b70)
 Call ID: e579559c-4e14-45dc-8e41-7ce463813b70
  Args:
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasRelation
    source: Prince_Nicholas_of_Greece_and_Denmark
  AssignClass (53b7f31a-c8a8-4187-a3df-ea93fb291600)
 Call ID: 53b7f31a-c8a8-4187-a3df-ea93fb291600
  Args:
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    type: :Man
  AssignClass (18dfe607-f292-4307-9cd5-2812c5c09fc2)
 Call ID: 18dfe607-f292-4307-9cd5-2812c5c09fc2
  Args:
    source: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    type: :Person
  AssignClass (8a4bf819-c285-4131-8b34-02010616e46f)
 Call ID: 8a4bf819-c285-4131-8b34-02010616e46f
  Args:
    type: :Woman
    source: Marie_of_Mecklenburg-Schwerin
  AssignClass (b6368d8e-30e4-4f82-bd43-3e324068a7d9)
 Call ID: b6368d8e-30e4-4f82-bd43-3e324068a7d9
  Args:
    source: Marie_of_Mecklenburg-Schwerin
    type: :Person
  AddTriple (997b8818-4566-41f1-8857-26cc1797ba53)
 Call ID: 997b8818-4566-41f1-8857-26cc1797ba53
  Args:
    target: Grand_Duke_Vladimir_Alexandrovich_of_Russia
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasFather
  AddTriple (637ffee5-c08b-4a3a-895b-58acfd134134)
 Call ID: 637ffee5-c08b-4a3a-895b-58acfd134134
  Args:
    target: Marie_of_Mecklenburg-Schwerin
    source: Grand_Duchess_Elena_Vladimirovna_of_Russia
    relation: :hasMother
  AssignClass (fd0ee6bb-d700-49a7-ba3b-25369279d4c0)
 Call ID: fd0ee6bb-d700-49a7-ba3b-25369279d4c0
  Args:
    type: :Man
    source: Grand_Duke_Kirill_Vladimirovich
  AssignClass (30a7f231-9ad4-4c48-ba70-d1f8d6f8a3ac)
 Call ID: 30a7f231-9ad4-4c48-ba70-d1f8d6f8a3ac
  Args:
    source: Grand_Duke_Kirill_Vladimirovich
    type: :Person
  AddTriple (a3d3ae60-ae1a-42a1-88af-6d98163392cf)
 Call ID: a3d3ae60-ae1a-42a1-88af-6d98163392cf
  Args:
    relation: :hasSister
    source: Grand_Duke_Kirill_Vladimirovich
    target: Grand_Duchess_Elena_Vladimirovna_of_Russia
  AssignClass (a1ff3640-43ad-40a5-a807-4847deb19c71)
 Call ID: a1ff3640-43ad-40a5-a807-4847deb19c71
  Args:
    source: Constantine
    type: :Man
  AssignClass (ec5c598d-9d3a-4d97-9858-1a6a7df1504e)
 Call ID: ec5c598d-9d3a-4d97-9858-1a6a7df1504e
  Args:
    source: Constantine
    type: :Person
  AssignClass (b1b6128f-d932-4073-b4c5-391e8f61914a)
 Call ID: b1b6128f-d932-4073-b4c5-391e8f61914a
  Args:
    source: George
    type: :Man
  AssignClass (9f0a55e3-3412-4bf3-b411-f6015a489c8f)
 Call ID: 9f0a55e3-3412-4bf3-b411-f6015a489c8f
  Args:
    type: :Person
    source: George
  AddTriple (598ad532-bf58-4e22-a9da-22b1b20469ed)
 Call ID: 598ad532-bf58-4e22-a9da-22b1b20469ed
  Args:
    target: Constantine
    relation: :hasBrother
    source: Prince_Nicholas_of_Greece_and_Denmark
  AddTriple (c5c21a60-f178-4015-80be-5d17ba9a91e1)
 Call ID: c5c21a60-f178-4015-80be-5d17ba9a91e1
  Args:
    relation: :hasBrother
    source: Prince_Nicholas_of_Greece_and_Denmark
    target: George
  AssignClass (90657e42-8526-4876-898c-8d17e4364ad4)
 Call ID: 90657e42-8526-4876-898c-8d17e4364ad4
  Args:
    source: George_Simitis
    type: :Man
  AssignClass (bf7a8060-3f11-4626-bc6a-0e8c0c13a47a)
 Call ID: bf7a8060-3f11-4626-bc6a-0e8c0c13a47a
  Args:
    type: :Person
    source: George_Simitis
  AssignClass (106a3a3d-9df5-4a21-8e66-fdefc3e3665a)
 Call ID: 106a3a3d-9df5-4a21-8e66-fdefc3e3665a
  Args:
    type: :Man
    source: Kostas_Simitis
  AssignClass (657dce4d-005e-4b83-85f1-db49da5582eb)
 Call ID: 657dce4d-005e-4b83-85f1-db49da5582eb
  Args:
    type: :Person
    source: Kostas_Simitis
  AddTriple (19029024-7be2-4130-9ab1-ccb87b09de57)
 Call ID: 19029024-7be2-4130-9ab1-ccb87b09de57
  Args:
    target: George_Simitis
    source: Kostas_Simitis
    relation: :hasFather
  Finish (8963481d-3e37-4f3b-a8d8-2192256d9114)
 Call ID: 8963481d-3e37-4f3b-a8d8-2192256d9114
  Args: