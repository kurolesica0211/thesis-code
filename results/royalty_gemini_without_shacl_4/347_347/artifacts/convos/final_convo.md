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
Ernst August von Hannover (German: Ernst August Albert Paul Otto Rupprecht Oskar Berthold Friedrich-Ferdinand Christian-Ludwig Prinz von Hannover Herzog zu Braunschweig und Lüneburg Königlicher Prinz von Großbritannien und Irland, lit.
'Ernest Augustus Albert Paul Otto Rupert Oscar Berthold Frederick-Ferdinand Christian-Louis, Prince of Hanover, Duke of Brunswick and Lüneburg, Royal Prince of Great Britain and Ireland'; born 26 February 1954) is the head of the House of Hanover, members of which reigned in Great Britain and Ireland from 1714 to 1901, the Kingdom of Hanover from 1814 to 1866 (electorate, from 1714 to 1814), and the Duchy of Brunswick from 1913 to 1918.
As the husband of Princess Caroline of Monaco, he is the brother-in-law of Albert II, Prince of Monaco.
Background and education

Ernst August was born in Hanover, the eldest son of Prince Ernest Augustus of Hanover (1914–1987), the former Hereditary Prince of Brunswick and his first wife, Princess Ortrud of Schleswig-Holstein-Sonderburg-Glücksburg (1925–1980).
He was christened Ernst August Albert Paul Otto Rupprecht Oskar Berthold Friedrich-Ferdinand Christian-Ludwig.
As the senior male-line descendant of George III of the United Kingdom, Ernst August is head of the House of Hanover.
Ancestry and heritage

The title of Prince of Great Britain and Ireland was recognised ad personam for Ernst August's father and his father's siblings by George V of the United Kingdom on 17 June 1914.
However, the title Royal Prince of Great Britain and Ireland had been entered into the family's German passports, together with the German titles, in 1914.
Ernst August continues to claim the style, "Royal Prince of Great Britain and Ireland".
However, in addition to being a German, Ernst August also has British citizenship since his father had successfully claimed it under the Sophia Naturalization Act 1705 (in the case of Attorney-General v. Prince Ernest Augustus of Hanover).
Since foreign royal titles can't be entered into a British passport, his father ended up being named Ernest Augustus Guelph, with the addition of His Royal Highness.
His children, including Ernst August, inherited British nationality under this name.
Marriage and family

First marriage

By a 24 August 1981 declaration issued by his father as the Head of House, pursuant to Chapter 3, §§ 3 and 5 of the House laws of 1836, Ernst August was authorised to marry dynastically, and did firstly marry, civilly in Pattensen on 28 August 1981 and religiously on 30 August 1981, Chantal Hochuli (born 2 June 1955 in Zürich), the daughter and heiress of a Swiss German architect and real estate developer, Johann Gustav "Hans" Hochuli (14 March 1912 in Switzerland – ?), and his German wife Rosmarie Lembeck (8 April 1921, in Essen, Rhine, Prussia, Germany – 12 December 2011).
They have two sons, Prince Ernst August (born 19 July 1983) and Prince Christian (born 1 June 1985).
Ernst August and Chantal Hochuli divorced in London on 23 October 1997.
In 1988, Ernst August unsuccessfully claimed custody of his infant nephew Otto Heinrich, son of his younger brother, Prince Ludwig Rudolph of Hanover.
Ludwig Rudolph placed a call to his brother in London, imploring him to take care of the couple's 10-month-old son, and shortly afterwards died by suicide.
Custody of Otto Heinrich was eventually awarded, contrary to the expressed wishes of Ludwig Rudolph as the surviving parent and Ernst August's legal efforts, to the child's maternal grandparents, Count Ariprand (1925–1996) and Countess Maria von Thurn und Valsassina-Como-Vercelli (born 1929), to be raised at their family seat, Bleiburg Castle in southern Austria.
Second marriage

Ernst August married secondly, civilly in Monaco on 23 January 1999, Princess Caroline of Monaco, who was at the time expecting their daughter, Princess Alexandra (born 20 July 1999).
As he was descended from George II of Great Britain in the male line, Ernst August sought and received permission to marry pursuant to the British Royal Marriages Act 1772, which would not be repealed until the Succession to the Crown Act 2013 took effect on 26 March 2015.
Similarly the Monégasque court officially notified the government of France of Caroline's marriage to Ernst August, receiving assurance that there was no objection in compliance with the (since defunct)
Moreover, in order for Caroline to retain her claim to the throne of Monaco and to transmit succession rights to future offspring, the couple were also obliged to obtain the approval of yet a third nation, in the form of official consent to the marriage of Caroline's father, Prince Rainier III, as the sovereign of Monaco.
After their marriage, Ernst August and Caroline moved to Le Mée-sur-Seine, France, where they had purchased an 18th-century manor house from their friend Karl Lagerfeld.
In 2009, it was reported that Caroline had separated from Ernst August and returned to live in Monaco.
Controversies

Assault on journalist

In 1999, Ernst August was accused of assaulting a journalist with an umbrella.
Turkish Pavilion

Ernst August was photographed urinating on the Turkish Pavilion at the Expo 2000 event in Hanover, causing a diplomatic incident and a complaint from the Turkish embassy accusing him of insulting the Turkish people.
Assault charge

In 2000, Ernst August was involved in a dispute with a German man, Joseph Brunnlehner, on the island of Lamu in Kenya.
Brunnlehner was the operator of a disco, and Ernst August allegedly assaulted him with a knuckleduster, upset about the noise coming from the disco.
Family property dispute

In 2004, Ernst August had signed over his German property to his elder son, including Marienburg Castle, the agricultural estate of Calenberg Castle, the "Princely House" at Herrenhausen Gardens in Hanover and some forests near Blankenburg Castle (Harz) which he had repurchased in former East Germany after the German reunification of 1990.
At the time, Ernst August's wealth was estimated as high as $250 million.
Since then, the younger Ernst August has taken over many representative tasks on behalf of his father.
In 2013, however, Ernst August was removed from the chairmanship of a family foundation based in Liechtenstein, the Duke of Cumberland Foundation, which holds the properties near Gmunden in Austria, the Hanovers' main residence in exile after 1866 when their Kingdom of Hanover was annexed by Prussia.
Instead, the younger Ernst August was put in charge, reportedly for negligence on part of his father, at the initiative of the foundation's trustee Prince Michael of Liechtenstein.
In 2017, Ernst August filed legal action to recover his chairmanship, and he intends to revoke the bestowal of his German property.
Assault on police

In 2020, under the influence of alcohol and medication, Ernst August injured a police officer at his hunting lodge in Austria.
Health

On Sunday, 3 April 2005, Ernst August was admitted to hospital with acute pancreatitis.
The next day, he fell into a deep coma, two days before the death of his father-in-law, Rainier III, Prince of Monaco.



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
  AssignClass (87127d3d-4c13-4f21-afbf-183cc9fb40b2)
 Call ID: 87127d3d-4c13-4f21-afbf-183cc9fb40b2
  Args:
    source: :ErnstAugustVonHannover
    type: :Man
  AssignClass (d2de2988-7234-487d-8cb6-6040b778c8f2)
 Call ID: d2de2988-7234-487d-8cb6-6040b778c8f2
  Args:
    type: :Person
    source: :ErnstAugustVonHannover
  AddLiteral (78d43a6e-72f8-42b4-a2df-a751bccfc3fc)
 Call ID: 78d43a6e-72f8-42b4-a2df-a751bccfc3fc
  Args:
    source: :ErnstAugustVonHannover
    relation: :hasBirthYear
    literal_value: 1954
    literal_type: xsd:positiveInteger
  AssignClass (e64841ca-59b5-442f-a6f1-5cc516799a0b)
 Call ID: e64841ca-59b5-442f-a6f1-5cc516799a0b
  Args:
    type: :Man
    source: :PrinceErnestAugustOfHannover
  AssignClass (4bbcae2f-8e13-414b-a2e3-e2ca4ad480dc)
 Call ID: 4bbcae2f-8e13-414b-a2e3-e2ca4ad480dc
  Args:
    type: :Person
    source: :PrinceErnestAugustOfHannover
  AddLiteral (516809ee-65e5-45f0-8cd9-7eda51c46e55)
 Call ID: 516809ee-65e5-45f0-8cd9-7eda51c46e55
  Args:
    literal_type: xsd:positiveInteger
    literal_value: 1914
    relation: :hasBirthYear
    source: :PrinceErnestAugustOfHannover
  AddLiteral (1c49b78e-86a0-4f40-8d76-a890936374dc)
 Call ID: 1c49b78e-86a0-4f40-8d76-a890936374dc
  Args:
    source: :PrinceErnestAugustOfHannover
    relation: :hasDeathYear
    literal_value: 1987
    literal_type: xsd:positiveInteger
  AssignClass (04bcc7da-7df0-4f4f-888c-032f7b0184f8)
 Call ID: 04bcc7da-7df0-4f4f-888c-032f7b0184f8
  Args:
    source: :PrincessOrtrudOfSchleswigHolsteinSonderburgGlucksburg
    type: :Woman
  AssignClass (c2d0af51-cee8-4228-8592-38c72e85e01d)
 Call ID: c2d0af51-cee8-4228-8592-38c72e85e01d
  Args:
    type: :Person
    source: :PrincessOrtrudOfSchleswigHolsteinSonderburgGlucksburg
  AddLiteral (9bf1b315-c8c9-458a-8e97-7ee88f104266)
 Call ID: 9bf1b315-c8c9-458a-8e97-7ee88f104266
  Args:
    source: :PrincessOrtrudOfSchleswigHolsteinSonderburgGlucksburg
    relation: :hasBirthYear
    literal_value: 1925
    literal_type: xsd:positiveInteger
  AddLiteral (b9dcb242-548c-472a-b1d9-e7a06079544e)
 Call ID: b9dcb242-548c-472a-b1d9-e7a06079544e
  Args:
    source: :PrincessOrtrudOfSchleswigHolsteinSonderburgGlucksburg
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
    literal_value: 1980
  AddTriple (27dd4c17-e2da-4bbd-81c4-9462ecd3841e)
 Call ID: 27dd4c17-e2da-4bbd-81c4-9462ecd3841e
  Args:
    relation: :hasFather
    source: :ErnstAugustVonHannover
    target: :PrinceErnestAugustOfHannover
  AddTriple (1f9d26e8-af26-4c51-bae8-6edef5d92f10)
 Call ID: 1f9d26e8-af26-4c51-bae8-6edef5d92f10
  Args:
    target: :PrincessOrtrudOfSchleswigHolsteinSonderburgGlucksburg
    source: :ErnstAugustVonHannover
    relation: :hasMother
  AssignClass (96518ce3-caf6-4197-ae01-c2a5a1ca73db)
 Call ID: 96518ce3-caf6-4197-ae01-c2a5a1ca73db
  Args:
    type: :Woman
    source: :ChantalHochuli
  AssignClass (8ed41b74-de34-465d-b3b4-5dadbfd7e109)
 Call ID: 8ed41b74-de34-465d-b3b4-5dadbfd7e109
  Args:
    type: :Person
    source: :ChantalHochuli
  AddLiteral (2a5e8c60-52d1-4ec5-a2ba-b53fdc98c41d)
 Call ID: 2a5e8c60-52d1-4ec5-a2ba-b53fdc98c41d
  Args:
    relation: :hasBirthYear
    literal_value: 1955
    literal_type: xsd:positiveInteger
    source: :ChantalHochuli
  AssignClass (0c73a622-d5db-4991-ba37-a02a8f60652b)
 Call ID: 0c73a622-d5db-4991-ba37-a02a8f60652b
  Args:
    type: :Man
    source: :PrinceErnstAugustJunior
  AssignClass (0ba70344-539f-4dcf-9100-71ad84238b6c)
 Call ID: 0ba70344-539f-4dcf-9100-71ad84238b6c
  Args:
    source: :PrinceErnstAugustJunior
    type: :Person
  AddLiteral (6bbcfa50-9249-40bb-87df-7c93d9890ace)
 Call ID: 6bbcfa50-9249-40bb-87df-7c93d9890ace
  Args:
    source: :PrinceErnstAugustJunior
    literal_value: 1983
    relation: :hasBirthYear
    literal_type: xsd:positiveInteger
  AssignClass (7b8998df-772a-4a44-8f6b-4ea023091652)
 Call ID: 7b8998df-772a-4a44-8f6b-4ea023091652
  Args:
    type: :Man
    source: :PrinceChristian
  AssignClass (83a35372-818b-432f-8afa-0a05eb26c3c9)
 Call ID: 83a35372-818b-432f-8afa-0a05eb26c3c9
  Args:
    source: :PrinceChristian
    type: :Person
  AddLiteral (5a662148-84d8-427b-bffc-1472f095b7f4)
 Call ID: 5a662148-84d8-427b-bffc-1472f095b7f4
  Args:
    source: :PrinceChristian
    relation: :hasBirthYear
    literal_value: 1985
    literal_type: xsd:positiveInteger
  AddTriple (3bf12234-3932-445b-bd17-acbf914f057d)
 Call ID: 3bf12234-3932-445b-bd17-acbf914f057d
  Args:
    target: :ErnstAugustVonHannover
    source: :PrinceErnstAugustJunior
    relation: :hasFather
  AddTriple (7092eeed-a37a-48da-b8e8-48558da02744)
 Call ID: 7092eeed-a37a-48da-b8e8-48558da02744
  Args:
    source: :PrinceErnstAugustJunior
    target: :ChantalHochuli
    relation: :hasMother
  AddTriple (93dd86c0-a240-4115-903f-3947997e2545)
 Call ID: 93dd86c0-a240-4115-903f-3947997e2545
  Args:
    relation: :hasFather
    source: :PrinceChristian
    target: :ErnstAugustVonHannover
  AddTriple (5f738519-b725-4ce0-ba9a-3486bc713498)
 Call ID: 5f738519-b725-4ce0-ba9a-3486bc713498
  Args:
    target: :ChantalHochuli
    source: :PrinceChristian
    relation: :hasMother
  AssignClass (1ffed45f-926c-4d76-8c13-b83ca5189f8a)
 Call ID: 1ffed45f-926c-4d76-8c13-b83ca5189f8a
  Args:
    source: :PrinceLudwigRudolphOfHannover
    type: :Man
  AssignClass (3078c297-40a2-4ba0-b01b-11c911730461)
 Call ID: 3078c297-40a2-4ba0-b01b-11c911730461
  Args:
    source: :PrinceLudwigRudolphOfHannover
    type: :Person
  AddTriple (e4cb035d-d9fb-402a-860d-caf721f8e626)
 Call ID: e4cb035d-d9fb-402a-860d-caf721f8e626
  Args:
    relation: :isBrotherOf
    target: :ErnstAugustVonHannover
    source: :PrinceLudwigRudolphOfHannover
  AssignClass (bda0af1e-abdd-4993-8bcc-54f8195b7c92)
 Call ID: bda0af1e-abdd-4993-8bcc-54f8195b7c92
  Args:
    type: :Man
    source: :OttoHeinrich
  AssignClass (aa7d2bde-1cc7-4f87-8b46-cacbf569f699)
 Call ID: aa7d2bde-1cc7-4f87-8b46-cacbf569f699
  Args:
    type: :Person
    source: :OttoHeinrich
  AddTriple (9efb72e1-2514-4911-9e26-32e8d656b30c)
 Call ID: 9efb72e1-2514-4911-9e26-32e8d656b30c
  Args:
    relation: :hasFather
    target: :PrinceLudwigRudolphOfHannover
    source: :OttoHeinrich
  AssignClass (3d919dcd-289e-480d-b117-13318179e0eb)
 Call ID: 3d919dcd-289e-480d-b117-13318179e0eb
  Args:
    type: :Woman
    source: :PrincessCarolineOfMonaco
  AssignClass (ffae5fe7-5b0c-4ed7-9248-66d4ea46ed20)
 Call ID: ffae5fe7-5b0c-4ed7-9248-66d4ea46ed20
  Args:
    type: :Person
    source: :PrincessCarolineOfMonaco
  AssignClass (fa704243-bad2-4b56-890f-ff1bf0dc95a4)
 Call ID: fa704243-bad2-4b56-890f-ff1bf0dc95a4
  Args:
    source: :PrincessAlexandra
    type: :Woman
  AssignClass (720f88ce-0927-4237-902b-37e917c9f782)
 Call ID: 720f88ce-0927-4237-902b-37e917c9f782
  Args:
    source: :PrincessAlexandra
    type: :Person
  AddLiteral (2f910faf-0497-4039-95d4-c0242eaa5dec)
 Call ID: 2f910faf-0497-4039-95d4-c0242eaa5dec
  Args:
    source: :PrincessAlexandra
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1999
  AddTriple (86cf9e33-726c-4635-b2b7-1ad2a253704a)
 Call ID: 86cf9e33-726c-4635-b2b7-1ad2a253704a
  Args:
    source: :PrincessAlexandra
    target: :ErnstAugustVonHannover
    relation: :hasFather
  AddTriple (84f5453e-e944-4b40-920c-476fd49b28ac)
 Call ID: 84f5453e-e944-4b40-920c-476fd49b28ac
  Args:
    relation: :hasMother
    source: :PrincessAlexandra
    target: :PrincessCarolineOfMonaco
  AssignClass (27547c02-d51d-4b80-b3f0-2fa528ee5145)
 Call ID: 27547c02-d51d-4b80-b3f0-2fa528ee5145
  Args:
    source: :PrinceRainierIII
    type: :Man
  AssignClass (6194de88-2414-4b19-9560-b24f1f58ef94)
 Call ID: 6194de88-2414-4b19-9560-b24f1f58ef94
  Args:
    source: :PrinceRainierIII
    type: :Person
  AddTriple (0c067723-43e2-4719-8d01-1e6989625cfc)
 Call ID: 0c067723-43e2-4719-8d01-1e6989625cfc
  Args:
    relation: :hasFather
    target: :PrinceRainierIII
    source: :PrincessCarolineOfMonaco
  AssignClass (805d4607-2338-40bd-836c-2d40707bf924)
 Call ID: 805d4607-2338-40bd-836c-2d40707bf924
  Args:
    type: :Man
    source: :JohannGustavHansHochuli
  AssignClass (1cd06a53-a2fe-4c1e-b1b2-819171d11f88)
 Call ID: 1cd06a53-a2fe-4c1e-b1b2-819171d11f88
  Args:
    type: :Person
    source: :JohannGustavHansHochuli
  AddLiteral (eaf48fd1-a2e0-475c-8b2a-c2dda8db3ea5)
 Call ID: eaf48fd1-a2e0-475c-8b2a-c2dda8db3ea5
  Args:
    source: :JohannGustavHansHochuli
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1912
  AssignClass (d81c0209-06e8-48ba-b1f8-f9e3cae48928)
 Call ID: d81c0209-06e8-48ba-b1f8-f9e3cae48928
  Args:
    source: :RosmarieLembeck
    type: :Woman
  AssignClass (7abc97d3-0add-475c-8458-2e34490515e4)
 Call ID: 7abc97d3-0add-475c-8458-2e34490515e4
  Args:
    source: :RosmarieLembeck
    type: :Person
  AddLiteral (e20c8fcd-d789-489e-9660-35df103ec66d)
 Call ID: e20c8fcd-d789-489e-9660-35df103ec66d
  Args:
    source: :RosmarieLembeck
    relation: :hasBirthYear
    literal_value: 1921
    literal_type: xsd:positiveInteger
  AddLiteral (ad3847c9-ee13-41fc-9e27-2a80bb941241)
 Call ID: ad3847c9-ee13-41fc-9e27-2a80bb941241
  Args:
    literal_value: 2011
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
    source: :RosmarieLembeck
  AddTriple (b89c2bfa-3324-48f2-a1b4-2e4b58cd1153)
 Call ID: b89c2bfa-3324-48f2-a1b4-2e4b58cd1153
  Args:
    relation: :hasFather
    source: :ChantalHochuli
    target: :JohannGustavHansHochuli
  AddTriple (a2011121-2cb7-4d8b-ab63-0c18afc17269)
 Call ID: a2011121-2cb7-4d8b-ab63-0c18afc17269
  Args:
    target: :RosmarieLembeck
    source: :ChantalHochuli
    relation: :hasMother
  AssignClass (1f5aa374-9fb9-4f37-b9f5-7e56fe7d5c14)
 Call ID: 1f5aa374-9fb9-4f37-b9f5-7e56fe7d5c14
  Args:
    type: :Man
    source: :CountAriprand
  AssignClass (a5943c84-9315-48fe-93bc-81e361d77e48)
 Call ID: a5943c84-9315-48fe-93bc-81e361d77e48
  Args:
    source: :CountAriprand
    type: :Person
  AddLiteral (cb8fcce9-ba24-4a87-a339-22b35722d0e7)
 Call ID: cb8fcce9-ba24-4a87-a339-22b35722d0e7
  Args:
    source: :CountAriprand
    relation: :hasBirthYear
    literal_value: 1925
    literal_type: xsd:positiveInteger
  AddLiteral (eb7ad568-97d0-4c61-8809-4d9a2f409e29)
 Call ID: eb7ad568-97d0-4c61-8809-4d9a2f409e29
  Args:
    source: :CountAriprand
    literal_value: 1996
    relation: :hasDeathYear
    literal_type: xsd:positiveInteger
  AssignClass (0740e22e-2278-467d-adf4-90cdcef4e205)
 Call ID: 0740e22e-2278-467d-adf4-90cdcef4e205
  Args:
    type: :Woman
    source: :CountessMariaVonThurnUndValsassinaComoVercelli
  AssignClass (e17f1f9c-8975-477c-9d84-254380bb1c3a)
 Call ID: e17f1f9c-8975-477c-9d84-254380bb1c3a
  Args:
    source: :CountessMariaVonThurnUndValsassinaComoVercelli
    type: :Person
  AddLiteral (8ccca572-8e06-4b8e-8caf-5a6d570530c2)
 Call ID: 8ccca572-8e06-4b8e-8caf-5a6d570530c2
  Args:
    source: :CountessMariaVonThurnUndValsassinaComoVercelli
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1929
  Finish (8880a64f-d29e-4280-ba12-bb66b0ea1604)
 Call ID: 8880a64f-d29e-4280-ba12-bb66b0ea1604
  Args: